from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify, sessions, g
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Cuisine, Ingredient, FlavorCompound, FlavorCompoundIngredient, IngredientSimilarity, IngredientSimCuisine

from sqlalchemy import func, desc
import json

app = Flask(__name__)
app.secret_key = "ABC"


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")


@app.route('/ingredients.json')
def ingredient_input():
    """This will populate the list of available ingredients in ingredient query form for Typeahead functionality."""

    ingredient_dict = {}

    for ingredient_inputs in Ingredient.query.all():

        ingredient_dict[ingredient_inputs.name] = ingredient_inputs.id
        
    return jsonify(ingredient_dict)


@app.route('/cuisines.json')
def cuisine_input():
    """This will populate the list of available cuisines in ingredient-cuisine query form for Typeahead functionality."""
    
    cuisine_dict = {}

    for cuisine_inputs in Cuisine.query.all():

        cuisine_dict[cuisine_inputs.name] = cuisine_inputs.id

    return jsonify(cuisine_dict)


@app.route("/ingredient_pairs")
def ingredient_pairs():
    """Show list of ingredients that pair with ingr_zero."""
    
    ingr_zero = str(request.args.get("ingr_zero_input")).rstrip()

    ingr_zero_id = Ingredient.query.filter(Ingredient.name==ingr_zero).all()[0].id

    ingr_zero_name = Ingredient.query.filter(Ingredient.name==ingr_zero).all()[0].name

    ingr_one_list = IngredientSimilarity.query.filter(IngredientSimilarity.ingr_zero == ingr_zero_id)\
                                        .order_by(desc(IngredientSimilarity.shared_fcs)).limit(10).all()

    ingr_one_names = []

    for ingr_similarity in ingr_one_list:

        ingr_one_id = ingr_similarity.ingr_one

        ingr_one_fcs = ingr_similarity.shared_fcs
        print "shared compounds is:" + str(ingr_one_fcs)

        ingr_one_name = Ingredient.query.filter(Ingredient.id==ingr_one_id).all()[0].name
        print "ingredient name is:" + str(ingr_one_name)

        ingr_fcs = (ingr_one_name, ingr_one_fcs)

        ingr_one_names.append(ingr_fcs)
    
    return render_template("ingredient_pairs.html", ingr_zero_name=ingr_zero_name,
                                                    ingr_one_fcs=ingr_one_fcs,
                                                    ingr_one_list=ingr_one_list,
                                                    ingr_one_names=ingr_one_names)


@app.route("/ingredient_pairs.json")
def ingredient_pairs_json():
    """Show list of ingredients that pair with ingr_zero."""
    
    data = {}

    ingr_zero = request.args.get("ingredient")

    ingr_zero_obj = Ingredient.query.filter(Ingredient.name==ingr_zero).first()
    print "ingr_zero_obj is ", ingr_zero_obj
    ingr_zero_id = ingr_zero_obj.id

    
    parent_name = ingr_zero_obj.name

    data["name"] = parent_name

    data["children"] = []

    ingr_one_list = IngredientSimilarity.query.filter(IngredientSimilarity.ingr_zero == ingr_zero_id)\
                                        .order_by(desc(IngredientSimilarity.shared_fcs)).limit(10).all()

    for  ingr_one in ingr_one_list:

        child = Ingredient.query.get(ingr_one.ingr_one).json()

        data["children"].append(child)

    return jsonify(data)



@app.route("/ingredient_pairs/cuisines")
def cuisine_ingredient_pairs():
    """Show list of ingredients that pair with ingr_zero, in a cuisine."""
    
    ingr_zero = request.args.get("ingr_zero_input").rstrip()
    cuisine = request.args.get("cuisine_input").rstrip()

    # print cuisine
    # print 50 * "%"

    ingr_zero_id = Ingredient.query.filter(Ingredient.name==ingr_zero).all()[0].id
    cuisine_id = Cuisine.query.filter(Cuisine.name==cuisine).all()[0].id


    ingr_sim_cuisine_results = []

    # for ingr_sim in ingr_one_list:

    ingr_one_sim_pairs = IngredientSimCuisine.query.filter(IngredientSimCuisine.ingr_zero==ingr_zero_id,\
                                                     IngredientSimCuisine.cuisine==cuisine_id)\
                                                     .order_by(desc(IngredientSimCuisine.count)).limit(10).all()
    
    # ingr_one_list = IngredientSimilarity.query.filter(IngredientSimilarity.ingr_zero == ingr_zero_id)\
    #                                     .order_by(desc(IngredientSimilarity.shared_fcs)).limit(10).all()
    print ingr_one_sim_pairs


    # print ingr_sim_cuisine_results

    # print "ingr_one_list is: " + str(ingr_one_list)
    # print len(ingr_one_list)
    
    return render_template("ingredient_pairs_cuisines.html", ingr_sim_cuisine_results=ingr_one_sim_pairs,
                                                             ingr_zero_name=ingr_zero,
                                                             cuisine=cuisine)


@app.route("/ingredient_pairs_cuisine.json")
def ingredient_pairs_cuisine_json():
    """Show list of ingredients that pair with ingr_zero in a cuisine."""

    data = {}
    # # print "jsonified data is : " + str(json.dumps(data))

    ingr_zero_name = request.args.get("ingredient")
    # # print 50 * "!"
    # print ingr_zero_name
    cuisine_name = request.args.get("cuisine")
    # # print cuisine_name
    # print "Cuisine is " + str(cuisine_name)
    # # print 50 * "@"

    # # ingr_zero_name = "banana"
    # # cuisine = "Italian"

    ingr_zero = Ingredient.query.filter(Ingredient.name==ingr_zero_name).first()
    ingr_zero_id = ingr_zero.id
    print "ingr_zero_id is:" + str(ingr_zero.id)


   

    cuisine_obj = Cuisine.query.filter(Cuisine.name==cuisine_name).first()
    # print cuisine_obj
    # print "Cuisine_obj is " + str(cuisine_obj)
    # print 10* "HAY LOOK HERE "
    # print "Cuisine_obj.id is " +str(cuisine_obj.id)
    cuisine_id = cuisine_obj.id
    # print "Cusine.name is " + str(cuisine_obj.name)
    # print 50 * "!"


    # parent_name = ingr_zero.name
    # cuisine_name = cuisine_obj.name

    # data["name"] = parent_name
    # # print "jsonified data is : " + str(json.dumps(data))

    # # data["children"] = cuisine_name
    # # print "jsonified data is : " + str(json.dumps(data))

    # # data["cluster"] = []
    # # print "jsonified data is : " + str(json.dumps(data))

    ingr_one_sim_pairs = IngredientSimCuisine.query.filter(IngredientSimCuisine.ingr_zero==ingr_zero_id,\
                                                     IngredientSimCuisine.cuisine==cuisine_id)\
                                                     .order_by(desc(IngredientSimCuisine.count)).limit(10).all()


    
    # print "ingr_one_sim_pairs is " + str(ingr_one_sim_pairs)

    ingr_one_ids = [ ingr_similarity.ingr_one for ingr_similarity in ingr_one_sim_pairs ]
    
    print "ingr_one_ids is " , ingr_one_ids
    # print "cuisine_id is" + str(cuisine_id)

    ingr_one_names = []

    for ingr_one_id in ingr_one_ids: 

        ingr_one_obj = Ingredient.query.filter(Ingredient.id==ingr_one_id).first()

        ingr_one_names.append(ingr_one_obj.name)

    print "ingr_one_names is:", ingr_one_names

    # inner_list = {}
    # inner_list["name"] = cuisine_name
    # inner_list["children"] = []

    # for ingr_one in ingr_one_ids:
    #     # the_id = ingr_one.id

    #     ingr_two_pairs_json = {}

    #     ingr_two_pairs = IngredientSimCuisine.query.filter(IngredientSimCuisine.ingr_zero==ingr_one,\
    #                                              IngredientSimCuisine.cuisine==cuisine_id)\
    #                                              .order_by(desc(IngredientSimCuisine.count)).limit(10).all()


    #     ingredient_one_matches = [ingr_sim_cuis.ingr_one_id.name for ingr_sim_cuis in ingr_two_pairs]
    #     print "INGREDIENT_ONE_MATCHES ARE: " , ingredient_one_matches
        
    #     single_leaf_data = ingredient_one_matches[1]
    #     leaf = {}
    #     leaf["name"] = single_leaf_data
    #     leaf["size"] = 1
    #     print "jsonified leaf is: " , ingredient_one_matches 


    #     # ingr_one["children"] = ingredient_one_matches

    #     # inner_list["children"].append(ingr_one.json())
    #     # print "ingr_one is: " , ingr_one 

    # print "INNER LIST IS: " + str(inner_list["children"])
    # # print "ingr_two_pairs is:" + str(ingr_two_pairs)

    # # ingr_two_pairs_json = {}
 
    # data["name"] = parent_name

  

    # for pair in ingr_one_sim_pairs:
        
    #     ingr_one = Ingredient.query.get(pair.ingr_one).json()
    #     # print "ingr_one is: " + str(ingr_one)
    #     # print "ingr_one count is: " + str(pair.count) 
    #     ingr_one["size"] = pair.count

    #     inner_list["children"].append(ingr_one.json())


        #print "ingr_one.name is: " + str(ingr_one.name)


        #pair = {"name": str(ingr_one.name), "size":1 }
        #rint "inner pair is: " + str(pair)

        #inner_list.append(ingr_one)

        # print "jsonified inner loop is : " + str(json.dumps(inner_list))



    # data["children"] = []
    # data["children"].append(inner_list)

    # ingr_one_list = IngredientSimilarity.query.filter(IngredientSimilarity.ingr_zero == ingr_zero_id)\
    #                                     .order_by(desc(IngredientSimilarity.shared_fcs)).limit(10).all()

    # for  ingr_one in ingr_one_list:

    #     child = Ingredient.query.get(ingr_one.ingr_one).json()

    #     data["children"].append(child)

    
    # data = 
    # cuisine_list["children"] = ingr_zero_list 
    # ingr_zero_list["children"] = ingr_one_list
    # ingr_one_list["children"] = []

    ingredient_zero_name = request.args.get("ingredient")
    # # print 50 * "!"
    # print ingr_zero_name
    cuisine_name = request.args.get("cuisine")

    # cuisine_name = "Italian"
    cuisine_size = 70000

    # ingredient_zero_name = "lemon"
    ingredient_zero_size = 100000

    def create_subtree(root_name, root_size, leaf_names, leaf_size):
        # creates a tree from Lists & Dicts that can be jsonified later

        leaf_objects = []

        for leaf_name in leaf_names:
            leaf = {}
            leaf["name"] = leaf_name
            leaf["size"] = leaf_size
            # print "leaf object is:", leaf

            leaf_objects.append(leaf)

        root = {}
        root["name"] = root_name
        root["size"] = root_size
        root["children"] = leaf_objects

        return root

    all_subtrees = []

    for ingr_one_id in ingr_one_ids:

        ingr_one_obj = Ingredient.query.filter(Ingredient.id==ingr_one_id).first()
        ingr_one_name = ingr_one_obj.name

        
        ingr_two_sim_pairs = IngredientSimCuisine.query.filter(IngredientSimCuisine.ingr_zero==ingr_one_id,\
                                                 IngredientSimCuisine.cuisine==cuisine_id)\
                                                 .order_by(desc(IngredientSimCuisine.count)).limit(10).all()


        print "ingr_one_sim_pairs is " + str(ingr_one_sim_pairs)

        ingr_two_ids = [ ingr_similarity.ingr_one for ingr_similarity in ingr_two_sim_pairs ]

        print "ingr_two_ids is " , ingr_two_ids

        ingr_two_names = []

        for ingr_two_id in ingr_two_ids: 

            ingr_two_obj = Ingredient.query.filter(Ingredient.id==ingr_two_id).first()

            ingr_two_names.append(ingr_two_obj.name)

        print "ingr_two_names is:", ingr_two_names

        sub_tree = create_subtree(ingr_one_name, 50000, ingr_two_names, 20000)

        all_subtrees.append(sub_tree)
    



    # sub_tree_2 = create_subtree(ingr_one_names[1], 20000, ["3", "4"], 10000)
    # sub_tree_3 = create_subtree(ingr_one_names[2], 20000, ["5", "6"], 10000)

    combined_subtrees = {}
    combined_subtrees["name"] = cuisine_name
    combined_subtrees["size"] = cuisine_size
    combined_subtrees["children"] = all_subtrees
    # combined_subtrees["children"] = [sub_tree_1, sub_tree_2, sub_tree_3]

    result = {}
    result["name"] = ingredient_zero_name
    result["size"] = ingredient_zero_size
    result["children"] = [combined_subtrees]

    data = result

    # one = {}
    # one["name"] = "1"
    # one["size"] = 10000

    # two = {}
    # two["name"] = "2"
    # two["size"] = 10000

    # A = {}
    # A["name"] = "A"
    # A["size"] = 20000

    # A_children = []
    # A_children.append(one)
    # A_children.append(two)
    # A["children"] = A_children   
    # A["children"] = [one, two]

    # data = A

    # data = {
    #     "name": "lemon", "size":50000,
    #     "children":[
    #         { "name":"Italian", "size":30000,
    #             "children":
    #             [
    #                 { "name":"A",
    #                    "children" : 
    #                    [ 
    #                         { "name":"1", "size":10000},
    #                         { "name":"2", "size":10000}
    #                    ]
    #                 },
    #                 { "name":"B",
    #                   "children": 
    #                     [
    #                         { "name":"3", "size":7000},
    #                         { "name":"4", "size":7000}
    #                     ]
    #                 },
    #                 { "name":"c",
    #                   "children": 
    #                     [
    #                         { "name":"5", "size":3000},
    #                         { "name":"6", "size":3000}
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }
     

    print data 

    return jsonify(data) 

# @app.route("/reingold_tilford")
# def ingredient_pairs_d3():
#     """Show tree diagram of ingredients that pair with ingr_zero."""

#     ingredient_zero = request.args.get("ingr_zero_input")

#     return render_template("reingold_tilford.html", ingr_zero=ingredient_zero)


# @app.route("/tree_cuisine")
# def ingredient_sim_cuisines_d3():
#     """Show tree diagram of ingredients that pair with ingr_zero in a cuisine."""

#     ingredient_zero = request.args.get("ingr_zero_input")
#     cuisine = request.args.get("cuisine_input")

#     return render_template("tree_cuisine.html", ingr_zero_name=ingredient_zero, cuisine=cuisine)

@app.route("/ingredients")
def ingredient_list():
    """Show list of all ingredients."""

    ingredients = Ingredient.query.order_by('name').all()
    
    return render_template(
        "ingredient_list.html",
         ingredients=ingredients
         )


@app.route("/ingredients/<int:id>")
def ingredient_detail(id):
    """Show the flavor compounds present in ingredient."""

    ingredient = Ingredient.query.get(id)
    fcis_list = FlavorCompoundIngredient.query.filter_by(ingredient_id=id).all()


    return render_template(
        "ingredient_detail.html", 
        ingredient=ingredient, 
        fcis_list=fcis_list
        )


@app.route("/flavorcompounds")
def flavorcompounds_list():
    """Show list of flavorcompounds."""

    flavorcompounds = FlavorCompound.query.order_by('name').all()
    return render_template(
        "flavorcompound_list.html", 
        flavorcompounds=flavorcompounds
        ) 


@app.route("/flavorcompounds/<int:id>")
def flavor_compound_detail(id):
    """Show the ingredients that contain the flavor compound."""

    flavorcompound = FlavorCompound.query.get(id)
    ingredients_list = FlavorCompoundIngredient.query.filter_by(compound_id=id).all()
    print ingredients_list 

    return render_template(
        "flavorcompound_detail.html",
        flavorcompound=flavorcompound,
        ingredients_list=ingredients_list
        )


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()

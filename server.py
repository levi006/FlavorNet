from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Cuisine, Ingredient, FlavorCompound, FlavorCompoundIngredient, IngredientSimilarity, IngredientSimCuisine

from sqlalchemy import func, desc
import json

app = Flask(__name__)
app.secret_key = "noms"


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

    ingr_zero_id = Ingredient.query.filter(Ingredient.name==ingr_zero).all()[0].id
    cuisine_id = Cuisine.query.filter(Cuisine.name==cuisine).all()[0].id

    ingr_sim_cuisine_results = []

    ingr_one_sim_pairs = IngredientSimCuisine.query.filter(IngredientSimCuisine.ingr_zero==ingr_zero_id,\
                                                     IngredientSimCuisine.cuisine==cuisine_id)\
                                                     .order_by(desc(IngredientSimCuisine.count)).limit(10).all()

    
    return render_template("ingredient_pairs_cuisines.html", ingr_sim_cuisine_results=ingr_one_sim_pairs,
                                                             ingr_zero_name=ingr_zero,
                                                             cuisine=cuisine)


@app.route("/ingredient_pairs_cuisine.json")
def ingredient_pairs_cuisine_json():
    """Show list of ingredients that pair with ingr_zero in a cuisine."""

    data = {}

    #user input for cuisine and their chosen ingredient, ingr_zero 
    ingr_zero_name = request.args.get("ingredient")

    cuisine_name = request.args.get("cuisine")


    ingr_zero = Ingredient.query.filter(Ingredient.name==ingr_zero_name).first()
    ingr_zero_id = ingr_zero.id
    print "ingr_zero_id is:" + str(ingr_zero.id)
   

    cuisine_obj = Cuisine.query.filter(Cuisine.name==cuisine_name).first()

    cuisine_id = cuisine_obj.id

    #Find ten most frequently paired ingredients (ingr one) to ingr zero within a cuisine 

    ingr_one_sim_pairs = IngredientSimCuisine.query.filter(IngredientSimCuisine.ingr_zero==ingr_zero_id,\
                                                     IngredientSimCuisine.cuisine==cuisine_id)\
                                                     .order_by(desc(IngredientSimCuisine.count)).limit(10).all()

    print "ingr_one_sim_pairs is " + str(ingr_one_sim_pairs)

    #Pull ingr one ids from similarity pair objects
    ingr_one_ids = [ ingr_similarity.ingr_one for ingr_similarity in ingr_one_sim_pairs ]
    
    print "ingr_one_ids is " , ingr_one_ids

    cuisine_size = 70000 #for d3 root sizes. 

    ingr_zero_size = 100000 #for d3 root sizes.

    def create_subtree(root_name, root_size, leaf_names, leaf_size):
        #helper function that creates a single layer tree using the flare.json format required for the Reingold-Tilford tree. 

        leaf_objects = []

        for leaf_name in leaf_names:
            leaf = {}
            leaf["name"] = leaf_name
            leaf["size"] = leaf_size

            leaf_objects.append(leaf)

        root = {}
        root["name"] = root_name
        root["size"] = root_size
        root["children"] = leaf_objects

        return root

    all_subtrees = []

    for ingr_one_id in ingr_one_ids:

        #Querying for the ingr_one_obj using the ingr_one_ids
        ingr_one_obj = Ingredient.query.filter(Ingredient.id==ingr_one_id).first()
        #Pulling the ingr_one_name from object
        ingr_one_name = ingr_one_obj.name

        #Querying for the ingr_two_sim_pairs using the ingr_one_ids
        ingr_two_sim_pairs = IngredientSimCuisine.query.filter(IngredientSimCuisine.ingr_zero==ingr_one_id,\
                                                 IngredientSimCuisine.cuisine==cuisine_id)\
                                                 .order_by(desc(IngredientSimCuisine.count)).limit(10).all()
        

        ingr_two_ids = [ ingr_similarity.ingr_one for ingr_similarity in ingr_two_sim_pairs ]

        print "ingr_two_ids is ", ingr_two_ids

        ingr_two_names = []

        #creates subtree of ingr_twos (the second tier of ingredient pairs)

        for ingr_two_id in ingr_two_ids: 

            #Querying for the ingr_two_objects using the ingr_two_ids 
            ingr_two_obj = Ingredient.query.filter(Ingredient.id==ingr_two_id).first()

            #Pulling the ingr_two names from the ingr_two_obj   
            ingr_two_names.append(ingr_two_obj.name)

        print "ingr_two_names is:", ingr_two_names

        #Calling helper function create_subtree
        sub_tree = create_subtree(ingr_one_name, 50000, ingr_two_names, 20000)

        all_subtrees.append(sub_tree)
    
    # Ensuing sub_trees should look like: sub_tree_2 =create_subtree(ingr_one_names[1], 20000, ["3", "4"], 10000)
    # And so on: sub_tree_3 = create_subtree(ingr_one_names[2], 20000, ["5", "6"], 10000)

    combined_subtrees = {}
    combined_subtrees["name"] = cuisine_name
    combined_subtrees["size"] = cuisine_size
    combined_subtrees["children"] = all_subtrees
    
    # All subsequent subtrees (1,2,3, etc.) will be appended to the list combined_subtrees:
    # combined_subtrees["children"] = [sub_tree_1, sub_tree_2, sub_tree_3]

    result = {}
    result["name"] = ingr_zero_name
    result["size"] = ingr_zero_size
    result["children"] = [combined_subtrees]

    data = result

    return jsonify(data) 

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

    app.debug = False

    connect_to_db(app)

    # DebugToolbarExtension(app)

    app.run()

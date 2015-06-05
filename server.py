from jinja2 import StrictUndefined

from flask import Flask, render_template, request, jsonify, sessions, g
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Cuisine, Ingredient, FlavorCompound, FlavorCompoundIngredient, IngredientSimilarity, IngredientSimCuisine

from sqlalchemy import func, desc

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
    print "ingr_zero is: '" + ingr_zero + "'"

    # ingr_zero = "black_tea"
    # print "ingr_zero is: " + ingr_zero 

    print 20 * "!"
    # print type(ingr_zero)

    ingr_zero_id = Ingredient.query.filter(Ingredient.name==ingr_zero).all()[0].id

    # print ingr_zero_id

    ingr_zero_name = Ingredient.query.filter(Ingredient.name==ingr_zero).all()[0].name
    # print ingr_zero_name

    # print "ingr_zero_id is: " + str(ingr_zero_id)

    ingr_one_list = IngredientSimilarity.query.filter(IngredientSimilarity.ingr_zero == ingr_zero_id)\
                                        .order_by(desc(IngredientSimilarity.shared_fcs)).limit(10).all()


    ingr_one_names = []

    for ingr_similarity in ingr_one_list:
        # print type(ingr_similarity)

        ingr_one_id = ingr_similarity.ingr_one
        # print "elem is: " + str(ingr_one_id)

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
    print 20 * ("%")
    # print ingr_zero
    # print type(ingr_zero)

    ingr_zero = request.args.get("ingredient")

    ingr_zero= Ingredient.query.filter(Ingredient.name==ingr_zero).first()
    ingr_zero_id = ingr_zero.id

    
    parent_name = ingr_zero.name

    data["name"] = parent_name
    #indexing the dictionary 

    data["children"] = []

    ingr_one_list = IngredientSimilarity.query.filter(IngredientSimilarity.ingr_zero == ingr_zero_id)\
                                        .order_by(desc(IngredientSimilarity.shared_fcs)).limit(10).all()

    for  ingr_one in ingr_one_list:

        child = Ingredient.query.get(ingr_one.ingr_one).json()

        data["children"].append(child)

    return jsonify(data)


@app.route("/ingredient_pairs_cuisine.json")
def ingredient_pairs_cuisine_json():
    """Show list of ingredients that pair with ingr_zero in a cuisine."""

    # data = {}

    # # ingr_zero = request.args.get("ingr_zero_input").rstrip()
    # # cuisine = request.args.get("cuisine_input").rstrip()

    # ingr_zero = "banana"
    # cuisine = "Italian"

    # ingr_zero = Ingredient.query.filter(Ingredient.name==ingr_zero).first()
    # ingr_zero_id = ingr_zero.id

    # cuisine = Cuisine.query.filter(Cuisine.name==cuisine).first()
    # cuisine_id = cuisine.id

    # parent_name = ingr_zero.name
    # cuisine_name = cuisine.name

    # data["ingr_zero_name"] = parent_name

    # data["cuisine"] = cuisine_name

    # data["ingr_one"] = []

    # ingr_one_sim_pairs = IngredientSimCuisine.query.filter(IngredientSimCuisine.ingr_zero==ingr_zero_id,\
    #                                                  IngredientSimCuisine.cuisine==cuisine_id)\
    #                                                  .order_by(desc(IngredientSimCuisine.count)).limit(25).all()
    # for ingr_one in ingr_one_sim_pairs:
        
    #     ingr_one = Ingredient.query.get(ingr_one.ingr_one).json()

    #     data["ingr_one"].append(ingr_one)


    data = {"ingr_one_name": "banana",
          "cuisine": "Italian", 
          "ingr_one": [
            {
              "id": 1257, 
              "name": "orange"
            }, 
            {
              "id": 1094, 
              "name": "raspberry"
            }, 
            {
              "id": 1399, 
              "name": "vanilla"
            }, 
            {
              "id": 1197, 
              "name": "apple"
            }, 
            {
              "id": 1179, 
              "name": "wheat"
            }, 
            {
              "id": 1160, 
              "name": "peanut"
            }, 
            {
              "id": 998, 
              "name": "olive_oil"
            }, 
            {
              "id": 1089, 
              "name": "rum"
            }
          ], 

        }

    return jsonify(data) 

# @app.route("/reingold_tilford")
# def ingredient_pairs_d3():
#     """Show tree diagram of ingredients that pair with ingr_zero."""

#     ingredient_zero = request.args.get("ingr_zero_input")

#     return render_template("reingold_tilford.html", ingr_zero=ingredient_zero)


@app.route("/tree_cuisine")
def ingredient_sim_cuisines_d3():
    """Show tree diagram of ingredients that pair with ingr_zero in a cuisine."""

    return render_template("tree_cuisine.html")


@app.route("/ingredient_pairs/cuisines")
def cuisine_ingredient_pairs():
    """Show list of ingredients that pair with ingr_zero, in a cuisine."""
    
    ingr_zero = request.args.get("ingr_zero_input").rstrip()
    cuisine = request.args.get("cuisine_input").rstrip()

    ingr_zero_id = Ingredient.query.filter(Ingredient.name==ingr_zero).all()[0].id
    cuisine_id = Cuisine.query.filter(Cuisine.name==cuisine).all()[0].id


    ingr_sim_cuisine_results = []

    # for ingr_sim in ingr_one_list:

    ingr_one_sim_pairs = IngredientSimCuisine.query.filter(IngredientSimCuisine.ingr_zero==ingr_zero_id,\
                                                     IngredientSimCuisine.cuisine==cuisine_id)\
                                                     .order_by(desc(IngredientSimCuisine.count)).limit(25).all()
    
    # ingr_one_list = IngredientSimilarity.query.filter(IngredientSimilarity.ingr_zero == ingr_zero_id)\
    #                                     .order_by(desc(IngredientSimilarity.shared_fcs)).limit(10).all()
    print ingr_one_sim_pairs


    # print ingr_sim_cuisine_results

    # print "ingr_one_list is: " + str(ingr_one_list)
    # print len(ingr_one_list)
    
    return render_template("ingredient_pairs_cuisines.html", ingr_sim_cuisine_results=ingr_one_sim_pairs,
                                                             ingr_zero_name=ingr_zero,
                                                             cuisine=cuisine)

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
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()

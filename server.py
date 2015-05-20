from jinja2 import StrictUndefined

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Ingredient, FlavorCompound, FlavorCompoundIngredient


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route('/')
def index():
    """Homepage."""
    ingr_zero = request.args.get("ingr_zero")
    cuisine = request.args.get("cuisine")

    return render_template("homepage.html")

@app.route("/ingredients")
def ingredient_list():
    """Show list of all ingredients."""

    ingredients = Ingredient.query.order_by('name').all()
    return render_template("ingredient_list.html", ingredients=ingredients)


@app.route("/ingredients/<int:id>")
def ingredient_detail(id):
    """Show the flavor compounds present in ingredient."""

    ingredient = Ingredient.query.get(id)
    fcis = FlavorCompoundIngredient.query.filter_by(ingredient_id=id).all()

    return render_template("ingredient_detail.html", 
                            ingredient=ingredient, 
                            fcis=fcis)


@app.route("/flavorcompounds")
def flavorcompounds_list():
    """Show list of flavorcompounds."""

    flavorcompounds = FlavorCompound.query.order_by().all()
    return render_template("flavorcompound_list.html", flavorcompounds=flavorcompounds)


@app.route("/flavorcompounds/<int:id>")
def flavor_compound_detail(id):
    """Show the ingredients that contain the flavor compound."""

    flavorcompound = FlavorCompound.query.get(id)
    ingredient = FlavorCompoundIngredient.query.filter_by(ingredient_id=id).all()
    return render_template("flavorcompound_detail.html",
                            flavorcompound=flavorcompound,
                            ingredient=ingredient)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()

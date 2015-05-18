from jinja2 import StrictUndefined

from flask import Flask, render_template

from model import connect_to_db, db, Ingredient, FlavorCompound


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/ingredients")
def ingredient_list():
    """Show list of ingredients."""

    ingredients = Ingredient.query.order_by('name').all()
    return render_template("ingredient_list.html", ingredients=ingredients)

@app.route("/ingredients/<int:ingredient_id>", methods=['GET'])
def ingredient_detail(ingredient_id):
    """Show the flavor compounds present in ingredient."""

    ingredient = Ingredient.query.get(id)

    return render_template("ingredient.html", ingredient=ingredient)

@app.route("/flavorcompounds")
def flavorcompounds_list():
    """Show list of flavorcompounds."""

    flavorcompounds = FlavorCompound.query.order_by('name').all()
    return render_template("flavorcompound_list.html", flavorcompounds=flavorcompounds)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)


    app.run()

"""Models and database functions for Flavornet project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Recipe(db.Model):
    """Recipe"""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredients = db.Column(db.String(64), nullable=True)
    region = db.Column(db.String(64), nullable=True)
    cuisine = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe recipe_id=%s region=%s ingredients=%s cuisine=%s>" % (
            self.recipe_id, self.region, self.cuisine)


class Region(db.Model):
    """Region(s) that a recipe or cuisine is associated with."""

    __tablename__ = "regions"

    region_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    cuisine = db.Column(db.String(50), nullaable=True) 
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Region region_id=%s name=%s cuisine=%s>" % (
            self.region_id, self.name, self.cuisine)


class Ingredient(db.Model):
    """Ingredients are individual components that make up recipes."""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Integer)
    flavor_compounds = db.Column(db.Integer)
    cuisine_id = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ingredient ingredient_id=%s name=%s flavor_compounds=%s cuisine=%s>" % (
            self.rating_id, self.movie_id, self.user_id, self.score)

class FlavorCompound(db.Model):
    """Flavour compounds make up the flavor profile of an individual ingredient and 
    contribute towards a recipe's flavor profile."""

    __tablename__ = "flavor_compounds"

    flavor_compound_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Integer)
    ingredient = db.Column(db.Integer)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<FlavorCompound flavorcompound_id=%s name=%s ingredient=%s>" % (
            self.flavorcompound_id, self.name, self.ingredient)

class Category(db.Model):
    """Categories are the food class of an ingredient, i.e. fruit, meat, plant, etc."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Integer)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s name=%s>" % (
            self.category, self.name)

class CuisineRegion(db.Model):
    """CuisineRegion is the relationship between cuisine and region. For example, 
    Canadian and Southwestern cuisines would be considered North American."""

    __tablename__ = "cuisine_region"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    region_id = db.Column(db.Integer)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Region region_id=%s name=%s cuisine=%s>" % (
            self.region_id, self.name, self.cuisine)

class IngredientsCategory(db.Model):
    """IngredientsCategory explicates the relationship between ingredients and what category they fall into."""

    __tablename__ = "ingredients_category"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_id = db.Column(db.Integer)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return pass        

class FlavorCompoundIngredient(db.Model):
    """FlavorCompoundIngredient relates the flavor compounds present in each ingredient."""

    __tablename__ = "flavor_compounds_ingredient"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    flavor_compound_id = db.Column(db.Integer)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return pass       
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
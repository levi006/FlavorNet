"""Models and database functions for Flavornet project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class Recipe(db.Model):
    """Recipe"""

    __tablename__ = "recipes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cuisine_id = db.Column(db.Integer, db.ForeignKey("cuisines.id"))
    
    cuisine = db.relationship("Cuisine",
                           backref=db.backref("recipes"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe recipe=%s cuisine=%s>" % (
            self.recipe, self.cuisine)


class Ingredient(db.Model):
    """Ingredients are individual components that make up recipes."""

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship("Category",
                            backref=db.backref("ingredients"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ingredient ingredient_id=%s name=%s >" % (
            self.ingredient_id, self.name)

class FlavorCompound(db.Model):
    """Flavour compounds make up the flavor profile of an individual ingredient and 
    contribute towards a recipe's flavor profile."""

    __tablename__ = "flavor_compounds"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<FlavorCompound flavor_compound_id=%s name=%s>" % (
            self.flavor_compound_id, self.name)


class Category(db.Model):
    """Categories are the food class of an ingredient, i.e. fruit, meat, plant, etc."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s name=%s>" % (
            self.name)


class FlavorCompoundIngredient(db.Model):
    """FlavorCompoundIngredient relates the flavor compounds present in each ingredient."""

    __tablename__ = "flavor_compounds_ingredient"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_id = db.Column(db.Integer)
    compound_id = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<FlavorCompoundIngredient flavor_compound_id= %s, ingredient_id= %s, compound_id= %s>" (
            self.flavor_compound_id, self.ingredient_id, self.compound_id)

class Cuisine(db.Model):
    """Recipes fall under Cuisines."""

    __tablename__ = "cuisines"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""
        
        return "<Cuisine cuisine_id=%s name=%s>" % (
            self.cuisine_id, self.name)

class Region(db.Model):
    """Region(s) that a recipe or cuisine is associated with."""

    __tablename__ = "regions"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False) 

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Region region_id=%s name=%s>" % (
            self.region_id, self.name)


class RecipeIngredient(db.Model):
    """RecipeIngredient is the relationship between recipes and their ingredients."""

    __tablename__ = "recipe_ingredients"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))

    
    recipe = db.relationship("Recipe",
                           backref=db.backref("recipe_ingredients"))


    ingredient = db.relationship("Ingredient",
                            backref=db.backref("recipe_ingredients"))
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe recipe_id=%s recipe_id=%s ingredient_id=%s>" % (
            self.recipe_ingredients_id, self.recipe_id, self.cuisine_id)     

      
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flavornet.db'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
   
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."

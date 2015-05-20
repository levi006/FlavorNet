"""Models and database functions for Flavornet project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
#import seed

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

        return "<Recipe id=%s cuisine=%s>" % (
            self.id, self.cuisine)

    def tearDown(self):
        table = Table('recipes', Base.metadata, autoload=True)
        table.drop(db.engine)
        table.create(db.engine)
        print "teardown complete for recipes"


class Ingredient(db.Model):
    """Ingredients are individual components that make up recipes."""

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    # fc_name= db.Column(db.Integer, db.ForeignKey('flavor_compounds.name'))

    # fc = db.relationship('FlavorCompound',
    #                         backref=db.backref('flavor_compounds'))
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    category = db.relationship("Category",
                             backref=db.backref("ingredients"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ingredient id=%s name=%s >" % (
            self.id, self.name)

    def tearDown(self):
        table = Table('ingredients', Base.metadata, autoload=True)
        table.drop(db.engine)
        table.create(db.engine)
        print "Teardown complete for ingredients"    

class FlavorCompound(db.Model):
    """Flavour compounds make up the flavor profile of an individual ingredient and 
    contribute towards a recipe's flavor profile."""

    __tablename__ = "flavor_compounds"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    # ingr_name= db.Column(db.Integer, db.ForeignKey("ingredient.name"))

    # ingredient = db.relationship('Ingredient',
    #                         backref=db.backref("flavor_compounds"))
    

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<FlavorCompound id=%s name=%s>" % (
            self.id, self.name)


class Category(db.Model):
    """Categories are the food class of an ingredient, i.e. fruit, meat, plant, etc."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category id=%s name=%s>" % (
            self.name)


class FlavorCompoundIngredient(db.Model):
    """FlavorCompoundIngredient relates the flavor compounds present in each ingredient."""

    __tablename__ = "flavor_compounds_ingredient"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    compound_id = db.Column(db.Integer, db.ForeignKey('flavor_compounds.id'))


    ingredient = db.relationship("Ingredient",
                           backref=db.backref("flavor_compounds_ingredients"))

    compound = db.relationship("FlavorCompound",
                            backref=db.backref("flavor_compounds_ingredients"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<FlavorCompoundIngredient id=%s, ingredient_id = %s, compound_id= %s >" % (
            self.id, self.ingredient_id, self.compound_id)

class Cuisine(db.Model):
    """Recipes fall under Cuisines."""

    __tablename__ = "cuisines"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""
        
        return "<Cuisine id=%s name=%s>" % (
            self.id, self.name)

    def teardown(self):
        table = Table('cuisines', Base.metadata, autoload=True)
        table.drop(db.engine)
        table.create(db.engine)
        print "Teardown complete for cuisines"

class Region(db.Model):
    """Region(s) that a recipe or cuisine is associated with."""

    __tablename__ = "regions"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False) 

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Region id=%s name=%s>" % (
            self.id, self.name)


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

    def tearDown(self):
        table = Table('recipe_ingredients', Base.metadata, autoload=True)
        table.drop(db.engine)
        table.create(db.engine)
        print "teardown complete for recipe_ingredients"
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe id=%s recipe_id=%s ingredient_id=%s>" % (
            self.id, self.recipe_id, self.ingredient_id)     

class IngredientSimiliarity(db.Model):
    """RecipeIngredient is the relationship between recipes and their ingredients."""

    __tablename__ = "ingredient_similarities"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingr_0 = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    ingr_1 = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    shared_fcs = db.Column(db.Integer, nullable=False)
    
    ingr_0 = db.relationship("Ingredient",
                           backref=db.backref("ingredient_similarties"))


    ingr_1 = db.relationship("Ingredient",
                            backref=db.backref("ingredient_similarities"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<IngredientSimiliarity id=%s ingr_0=%s ingr_1=%s shared_fcs=%s>" % (
        self.id, self.ingr_0, self.ingr_1, self.shared_fcs)
  
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

    Base = declarative_base()
    Base.metadata.bind = db.engine
    print "Connected to DB."

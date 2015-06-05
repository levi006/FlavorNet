"""Models and database functions for Flavornet project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
# import seed

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

    def json(self):

        json_ingr_sims = {}

        json_ingr_sims["id"] = self.id 

        json_ingr_sims["name"] = self.name 

        return json_ingr_sims

class FlavorCompound(db.Model):
    """Flavour compounds make up the flavor profile of an individual ingredient and 
    contribute towards a recipe's flavor profile."""

    __tablename__ = "flavor_compounds"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    ingredients = db.relationship("Ingredient", 
                            secondary="flavor_compounds_ingredient",
                            backref=db.backref("flavor_compounds")) #classname, table, table

    
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

class IngredientSimilarity(db.Model):
    """Tracks how many compounds two ingredients have in common."""

    __tablename__ = "ingredient_similarities"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingr_zero = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    ingr_one = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    shared_fcs = db.Column(db.Integer, nullable=False)
    
    # ingr_zero = db.relationship("Ingredient",
    #                        backref=db.backref("ingredient_similarities"))


    # ingr_one = db.relationship("Ingredient",
    #                         backref=db.backref("ingredient_similarities"))

    def __repr__(self):
        
        """Provide helpful representation when printed."""

        return "<IngredientSimilarity id=%s ingr_zero=%s ingr_one=%s shared_fcs=%s>" % (
        self.id, self.ingr_zero, self.ingr_one, self.shared_fcs)

class IngredientSimCuisine(db.Model):
    """ is the relationship between recipes and their ingredients."""

    __tablename__ = "ingr_sims_in_cuisines"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingr_zero = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    ingr_one = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    cuisine = db.Column(db.Integer, db.ForeignKey('cuisines.id'))
    count = db.Column(db.Integer, nullable=False, default=1)
    
    ingr_zero_id = db.relationship("Ingredient",
                           foreign_keys='IngredientSimCuisine.ingr_zero')

    ingr_one_id = db.relationship("Ingredient",
                            foreign_keys='IngredientSimCuisine.ingr_one')

    cuisine_id = db.relationship("Cuisine",
                            backref=db.backref("ingr_sims_in_cuisines"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<IngredientSimCuisine id=%s ingr_zero=%s ingr_one=%s cuisine=%s count=%s>" % (
        self.id, self.ingr_zero, self.ingr_one, self.cuisine, self.count)
  
    def tearDown(self):
        table = Table('ingr_sims_in_cuisines', Base.metadata, autoload=True)
        table.drop(db.engine)
        table.create(db.engine)
        print "teardown complete for ingr_sims_in_cuisines"  

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flavornet.db'
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
   
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)

    Base = declarative_base()
    Base.metadata.bind = db.engine
    print "Connected to DB."

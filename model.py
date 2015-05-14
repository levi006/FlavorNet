"""Models and database functions for Flavornet project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

# class Recipe(db.Model):
#     """Recipe"""

#     __tablename__ = "recipes"

#     recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     cuisine = db.Column(db.String(64), nullable=True, unique=True)
    
#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Recipe recipe=%s cuisine=%s>" % (
#             self.recipe, self.cuisine)


class Ingredient(db.Model):
    """Ingredients are individual components that make up recipes."""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ingredient ingredient_id=%s name=%s >" % (
            self.ingredient_id, self.name)

class FlavorCompound(db.Model):
    """Flavour compounds make up the flavor profile of an individual ingredient and 
    contribute towards a recipe's flavor profile."""

    __tablename__ = "flavor_compounds"

    flavor_compound_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<FlavorCompound flavor_compound_id=%s name=%s>" % (
            self.flavor_compound_id, self.name)


class Category(db.Model):
    """Categories are the food class of an ingredient, i.e. fruit, meat, plant, etc."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s name=%s>" % (
            self.name)


# class IngredientsCategory(db.Model):
#     """IngredientsCategory classifies the relationship between ingredients and what category they fall into."""

#     __tablename__ = "ingredients_category"

#     ingredient_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
#     category_id = db.Column(
#         db.Integer,
#         db.ForeignKey('categories.category_id'))
    
#     category = db.relationship(
#           'Category',
#            backref=db.backref('ingredients_category', order_by=id))


#     ingredient_id = db.Column(
#         db.Integer,
#         db.ForeignKey('ingredients.ingredient_id'))
    
#     ingredient = db.relationship(
#           'ingredient',
#            backref=db.backref('ingredients', order_by=id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#        return  

class FlavorCompoundIngredient(db.Model):
    """FlavorCompoundIngredient relates the flavor compounds present in each ingredient."""

    __tablename__ = "flavor_compounds_ingredient"

    flavor_compound_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_id = db.Column(db.Integer)
    compound_id = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<FlavorCompoundIngredient flavor_compound_id= %s, ingredient_id= %s, compound_id= %s>" (
            self.flavor_compound_id, self.ingredient_id, self.compound_id)

class Cuisine(db.Model):
    """Recipes fall under Cuisines."""

    __tablename__ = "cuisines"

    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""
        
        return "<Cuisine cuisine_id=%s name=%s>" % (
            self.cuisine_id, self.name)

class Region(db.Model):
    """Region(s) that a recipe or cuisine is associated with."""

    __tablename__ = "regions"

    region_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False) 

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Region region_id=%s name=%s>" % (
            self.region_id, self.name)


# class CuisineRegion(db.Model):
#     """CuisineRegion is the relationship between cuisine and region. For example, 
#     Canadian and Southwestern cuisines would be considered North American."""

#     __tablename__ = "cuisine_region"

#     category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     region_id = db.Column(db.Integer)
    
#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Region region_id=%s name=%s cuisine=%s>" % (
#             self.region_id, self.name, self.cuisine)     


      
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""
    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flavornet.db'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
   
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."

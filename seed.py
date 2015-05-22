"""Utility file to seed flavors database from Ahn datasets in seed_data/"""

from model import Recipe, RecipeIngredient, Ingredient, FlavorCompound, Category, FlavorCompoundIngredient, Cuisine, Region, connect_to_db, db
from server import app
from sqlalchemy import func


def parse_all_recipe_files():
    """Load multiple recipe files."""

    #If you have an unwieldy number of files, put them in a directory and iterate over files.
     
    recipe_file1 = "./seed_data/epic_recipes.txt"
    recipe_file2 = "./seed_data/menu_recipes.txt" 
    recipe_file3 = "./seed_data/allr_recipes.txt"

    load_recipes_from_file(recipe_file1)
    load_recipes_from_file(recipe_file2)
    load_recipes_from_file(recipe_file3)


def load_recipes_from_file(recipe_filename):
    """Load all recipes into database."""

    for row in open(recipe_filename):
        recipe_info = row.rstrip().split("\t")

        # print recipe_info 
        
        cuisine, ingredients_list = recipe_info[0], recipe_info[1:]

        cuisine_obj = Cuisine.query.filter_by(name = cuisine).first()

        if cuisine_obj:
            # cuisine_id = cuisine_obj.cuisine_id

            recipe = Recipe(cuisine_id=cuisine_obj.id)
            db.session.add(recipe)
        
        db.session.commit()

        for ingredient_row in ingredients_list:
            ingredient = ingredient_row[:]

            ingredient_obj = Ingredient.query.filter_by(name = ingredient).first()

            if ingredient_obj:
                recipe_ingredient = RecipeIngredient(ingredient_id = ingredient_obj.id, recipe_id = recipe.id)
                db.session.add(recipe_ingredient)
        db.session.commit()             
 
def load_ingredients():
    """Load all categories."""

    ingredients_file = open("./seed_data/ingr_info.tsv")

    for row in ingredients_file:
        ingredient_info = row.strip().split("\t")

        ingredient_id, name = int(ingredient_info[0]), ingredient_info[1]  

        print (ingredient_id)
        print (name) 

        ingredient = Ingredient(id=ingredient_id, name=name)
        db.session.add(ingredient)
    
    db.session.commit()   

def load_flavorcompounds():
    """Load flavor compounds from comp_info.tsv into database."""

    flavor_compounds_file= open("./seed_data/comp_info.tsv")

    for row in flavor_compounds_file:
        compound_info = row.strip().split("\t")

        compound_id, name = int(compound_info[0]), compound_info[1]
        
        #print type(compound_id)
        #print name 

        FC_id = FlavorCompound(id=compound_id, name=name)
        db.session.add(FC_id)

    db.session.commit()

def load_categories():
    """Load all categories."""

    categories_file = open("./seed_data/ingr_info.tsv")

    for row in categories_file:
        categories_info = row.strip().split("\t")

        name = categories_info[2]
   
        #print ingredient, category   

        category = Category(name=name)
        db.session.add(category)
    
    db.session.commit() 

def load_compounds_to_ingredient():
    """Load ingredients to flavor compounds information."""

    ingr_comp_file = open("./seed_data/ingr_comp.tsv")

    for row in ingr_comp_file:
        ingr_comp_info = row.strip().split("\t")

        ingredient_id, compound_id = ingr_comp_info[0], ingr_comp_info[1]
   

        #print ingredient_id, compound_id   

        compound_ingredient = FlavorCompoundIngredient(ingredient_id=ingredient_id, compound_id=compound_id)
        db.session.add(compound_ingredient)
    
    db.session.commit()


def load_cuisines():
    """Load all cuisines."""

    cuisines_file = open("./seed_data/map.txt")

    for row in cuisines_file:
        cuisine_info = row.strip().split("\t")

        cuisine_name, region = cuisine_info[0], cuisine_info[1]

        if cuisine_info[1] == None:
            cuisine_info = NULL
   
        #print cuisine, region
        cuisine = Cuisine(name=cuisine_name)
    
        db.session.add(cuisine)
    
    db.session.commit() 

def load_regions():
    """Load all regions."""

    regions_file = open("./seed_data/map.txt")

    for row in regions_file:
        regions_info = row.strip().split("\t")

        cuisine, region_name = regions_info[0], regions_info[1]

        if regions_info[1] == None:
            regions_info = NULL

        #print cuisine, region

        region = Region(name=region_name) 
        db.session.add(region)
    
    db.session.commit()  


def load_ingredient_similarities():

    i = 1

ingredients = Ingredient.query(func.count(id=i))
# print ingredients

for i in range(ingredients):

    ingr_input = Ingredient.query.filter_by(id=i).all() #returns list of compounds
    ingr_zero = IngredientSimiliarity(ingr_zero=ingr_input)

    db.session.add(ingr_zero)
    # db.session.commit()
    
    for j in range(ingredients):
        j = j + 1

        ingr_input_two = Ingredient.query.filter_by(id=j).first()
        ingr_one = IngredientSimilarity(ingr_one=ingr_input_two)

    # print ingr_zero
    # print ingr_one

        db.session.add(ingr_one)
        # db.session.commit()

    shared_compounds = len(set(ingr_zero[0].flavor_compounds) & set(ingr_one[0].flavor_compounds))
    shared_compounds = IngredientSimilarity(shared_compounds=shared_compounds)

    db.session.add(shared_compounds)

    db.session.commit()    
 
if __name__ == "__main__":
    connect_to_db(app)

    # parse_all_recipe_files()
    # load_recipes_from_file()
    # load_flavorcompounds()
    # load_compounds_to_ingredient()
    # load_ingredients()
    # load_categories()
    # load_cuisines()
    # load_regions()
    load_ingredient_similarities()
   

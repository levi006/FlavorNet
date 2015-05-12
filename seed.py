"""Utility file to seed flavors database from Ahn datasets in seed_data/"""

# from model import Recipe, Region, Ingredients, FlavorCompounds, Category, Ingredients_FlavorCompounds, Ingredients_Category, Recipes_Region, connect_to_db, db
# from server import app



def load_all_recipe_files():
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
    
    #recipes_file = open("./seed_data/epic_recipes.txt") #1/3 recipe files loaded here. Possible to unpack more than one file at a time?

    for row in open(recipe_filename):
        recipe_info = row.rstrip().split("\t")
        
        cuisine = recipe_info[0]    
        ingredient = recipe_info[1:]    
         
        print cuisine
        print ingredient       
     
#       #QUERY = "INSERT INTO  VALUES(user_id, email, password, age, zipcode)"
#         db.session.add(user)
    
#     db.session.commit()
    

def load_flavorcompounds():
    """Load flavor compounds from comp_info.tsv into database."""

    compound_file= open("./seed_data/comp_info.tsv")

    for row in compound_file:
        compound_info = row.strip().split("\t")

        compound_id = compound_info[0]
        name = compound_info[1]
        
        print compound_id
        print name 

    #   compound_id = FlavorCompounds(compound_id=compound_id, name=name)
    #   db.session.add(compound_id)

    # db.session.commit()

#def load_categories():
#     """Load ratings from u.data into database."""
    
#     data_file = open("seed_data/u.data")

#     for row in data_file:
#         if row:
#             data_info = row.strip().split()
#             user_id = data_info[0]    
#             movie_id = data_info[1]    
#             score = data_info[2]
#             #timestamp = data_info[3]

#             #timestamp = timestamp.datetime.strptime(t_timestamp, ) #add something behind the trailing comma
                    
#             rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#             db.session.add(rating)
    
#     db.session.commit()
   

if __name__ == "__main__":
#     connect_to_db(app)

    load_all_recipe_files()
    #load_recipes_from_files()
    # load_movies()
    # load_ratings()
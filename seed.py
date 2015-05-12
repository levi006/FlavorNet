"""Utility file to seed flavors database from Ahn datasets in seed_data/"""

# from model import Recipe, Region, Ingredients, FlavorCompounds, Category, Ingredients_FlavorCompounds, Ingredients_Category, Recipes_Region, connect_to_db, db
# from server import app



def load_recipes():
    """Load recipes into database."""
    
    recipes_file = open("./seed_data/epic_recipes.txt")

    for row in recipes_file:
        recipe_info = row.rstrip().split("\t")
        
        cuisine = recipe_info[0]    
        ingredient = recipe_info[1:]    
         
        print cuisine
        print ingredient       
    
        recipes 
#       #QUERY = "INSERT INTO  VALUES(user_id, email, password, age, zipcode)"
#         db.session.add(user)
    
#     db.session.commit()
    

def load_flavorcompounds():
    """Load flavorcompounds from comp_info.tsv into database."""

    compound_file= open("./seed_data/comp_info.tsv")

    for row in compound_file:
        compound_info = row.strip().split("\t")

        compound_id = compound_info[0]
        name = compound_info[1]
        
        print compound_id
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
    #     db.session.add(compound)

    # db.session.commit()

# def load_ratings():
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

    #load_recipes()
    load_flavorcompounds()
    # load_movies()
    # load_ratings()
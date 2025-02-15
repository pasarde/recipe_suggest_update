from dotenv import load_dotenv
import os
import requests
import pandas as pd

# Load Environment Variables
load_dotenv() 
API_KEY = os.getenv("SPOONACULAR_KEY")

def fetch_recipes(query="pasta", max_recipes=50):
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&query={query}&number={max_recipes}&addRecipeInformation=True"
    response = requests.get(url)
    recipes = response.json()["results"]
    
    # Convert to DataFrame
    df = pd.DataFrame([{
        "title": recipe["title"],
        "ingredients": ", ".join([ingr["name"] for ingr in recipe["extendedIngredients"]]),  # Fixed here
        "dietary": "vegetarian" if recipe["vegetarian"] else "non-vegetarian"
    } for recipe in recipes])
    
    df.to_csv("data/raw/recipes.csv", index=False)
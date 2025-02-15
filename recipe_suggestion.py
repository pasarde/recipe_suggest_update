# recipe_rec.py
import os
import requests
from dotenv import load_dotenv

# Load your Spoonacular API key from .env or environment variable
load_dotenv()
API_KEY = os.getenv("SPOONACULAR_KEY")

def suggest_recipes_by_ingredients(ingredients, number=5):
    """
    Suggest recipes based on a comma-separated string of ingredients.
    
    Parameters:
        ingredients (str): A comma-separated list of ingredients.
        number (int): Number of recipes to return (default is 5).
        
    Returns:
        list: A list of dictionaries containing recipe information.
    """
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "includeIngredients": ingredients,  # Filter by the ingredients provided
        "number": number,
        "addRecipeInformation": True       # Include extra details in the response
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("Error fetching recipes:", response.status_code, response.text)
        return []
    
    data = response.json()
    recipes = data.get("results", [])
    return recipes

def display_recipes(recipes):
    """
    Display details for each recipe.
    """
    if not recipes:
        print("No recipes found.")
        return

    for recipe in recipes:
        print("Title:", recipe.get("title", "N/A"))
        print("Ready in Minutes:", recipe.get("readyInMinutes", "N/A"))
        print("Servings:", recipe.get("servings", "N/A"))
        print("Source URL:", recipe.get("sourceUrl", "N/A"))
        print("Summary:", recipe.get("summary", "N/A"))
        print("Image URL:", recipe.get("image", "N/A"))
        print("-" * 40)

if __name__ == "__main__":
    # Prompt the user for ingredients
    user_ingredients = input("Enter the ingredients you have (comma-separated): ").strip()
    
    # Get recipe suggestions based on user input
    recipes = suggest_recipes_by_ingredients(user_ingredients, number=5)
    
    # Display the recipe suggestions
    display_recipes(recipes)
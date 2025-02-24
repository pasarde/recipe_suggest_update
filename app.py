import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load your Spoonacular API key from the .env file
load_dotenv()
API_KEY = os.getenv("SPOONACULAR_KEY")

app = Flask(__name__)

def suggest_recipes_by_ingredients(ingredients, number=5):
    """
    Call the Spoonacular API to get recipe suggestions based on ingredients.
    """
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "includeIngredients": ingredients,
        "number": number,
        "addRecipeInformation": True
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error fetching recipes:", response.status_code, response.text)
        return []
    data = response.json()
    return data.get("results", [])

def get_recipe_by_id(recipe_id):
    """
    Get detailed recipe information by ID
    """
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.json()

@app.route("/api/suggest", methods=["GET"])
def suggest():
    """
    API endpoint to suggest recipes.
    Pass the ingredients as a query parameter
    """
    ingredients = request.args.get("ingredients", "")
    if not ingredients:
        return jsonify({"error": "No ingredients provided."}), 400
    recipes = suggest_recipes_by_ingredients(ingredients)
    return jsonify(recipes)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    """
    Display detailed recipe information
    """
    recipe_data = get_recipe_by_id(recipe_id)
    if recipe_data is None:
        return "Recipe not found", 404
    return render_template("recipe.html", recipe=recipe_data)

@app.route("/")
def index():
    """
    Render the frontend page.
    """
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
import os
import requests
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
from database import init_db

# Load your Spoonacular API key from the .env file
load_dotenv()
API_KEY = os.getenv("SPOONACULAR_KEY")

app = Flask(__name__)
init_db()

def get_db():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

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
    recipes = data.get("results", [])
    
    # Get liked recipes and put them first
    db = get_db()
    liked = db.execute("SELECT recipe_id FROM likes").fetchall()
    liked_ids = [r['recipe_id'] for r in liked]
    
    # Reorder recipes to put liked ones first
    recipes.sort(key=lambda x: x['id'] in liked_ids, reverse=True)
    
    db.close()
    return recipes

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

@app.route("/favorite/<int:recipe_id>", methods=["POST"])
def add_favorite(recipe_id):
    recipe_data = get_recipe_by_id(recipe_id)
    if recipe_data:
        db = get_db()
        db.execute(
            "INSERT OR REPLACE INTO favorites (recipe_id, title, image, ready_in_minutes, servings) VALUES (?, ?, ?, ?, ?)",
            (recipe_id, recipe_data['title'], recipe_data['image'], recipe_data['readyInMinutes'], recipe_data['servings'])
        )
        db.commit()
        db.close()
    return redirect(url_for('recipe', recipe_id=recipe_id))

@app.route("/like/<int:recipe_id>", methods=["POST"])
def like_recipe(recipe_id):
    recipe_data = get_recipe_by_id(recipe_id)
    if recipe_data:
        db = get_db()
        db.execute(
            "INSERT OR REPLACE INTO likes (recipe_id, title) VALUES (?, ?)",
            (recipe_id, recipe_data['title'])
        )
        db.commit()
        db.close()
    return redirect(url_for('recipe', recipe_id=recipe_id))

@app.route("/favorites")
def favorites():
    db = get_db()
    favorites = db.execute("SELECT * FROM favorites").fetchall()
    db.close()
    return render_template("favorite.html", recipes=favorites)

@app.route("/")
def index():
    """
    Render the frontend page.
    """
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
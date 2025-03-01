import os
import requests
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
from database import init_db
from datetime import datetime
import random  # Tambahkan import ini di bagian atas file

# Load your Spoonacular API key from the .env file
load_dotenv()
API_KEY = os.getenv("SPOONACULAR_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_KEY")

app = Flask(__name__)
init_db()

def get_db():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_coordinates_by_city(city_name):
    """Get coordinates (latitude, longitude) for a given city name"""
    url = f"http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city_name,
        "limit": 1,
        "appid": WEATHER_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return str(data[0]['lat']), str(data[0]['lon'])
    except Exception as e:
        print(f"Error getting coordinates: {e}")
    return None

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

def get_weather_recommendations(city="Jakarta"):
    """Get weather data and return appropriate recipe recommendations"""
    print(f"Getting weather recommendations for {city}")
    
    try:
        # Get coordinates
        coordinates = get_coordinates_by_city(city)
        if coordinates:
            lat, lon = coordinates
            print(f"Found coordinates for {city}: {lat}, {lon}")
        else:
            lat, lon = "-6.2088", "106.8456"
            print(f"Using default Jakarta coordinates")

        # Get weather data
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        
        weather_response = requests.get(weather_url, weather_params)
        print(f"Weather API response status: {weather_response.status_code}")
        
        if weather_response.status_code != 200:
            print(f"Weather API error: {weather_response.text}")
            return None
            
        weather_data = weather_response.json()
        temp = weather_data['main']['temp']
        weather_condition = weather_data['weather'][0]['main'].lower()
        city_name = weather_data['name']
        
        print(f"Weather condition: {weather_condition}")
        print(f"Temperature: {temp}°C")
        
        # Define recipe queries with simpler queries
        weather_recipes = {
            'rain': {
                'query': 'soup',
                'message': f'Hujan di {city_name}! Ini rekomendasi makanan hangat yang cocok:'
            },
            'clear': {
                'query': 'salad',
                'message': f'Cerah di {city_name}! Ini rekomendasi makanan segar:'
            },
            'clouds': {
                'query': 'pasta',
                'message': f'Mendung di {city_name}. Ini rekomendasi comfort food:'
            }
        }
        
        # Get recommendation based on weather condition
        recommendation = weather_recipes.get(weather_condition, {
            'query': 'popular',
            'message': f'Rekomendasi makanan untuk {city_name} hari ini:'
        })
        
        print(f"Using query: {recommendation['query']}")
        
        # Get recipes from Spoonacular
        recipe_url = "https://api.spoonacular.com/recipes/complexSearch"
        recipe_params = {
            "apiKey": API_KEY,
            "query": recommendation['query'],
            "number": 20,
            "addRecipeInformation": True,
            "instructionsRequired": True,
            "fillIngredients": True
        }
        
        recipe_response = requests.get(recipe_url, recipe_params)
        print(f"Recipe API response status: {recipe_response.status_code}")
        
        if recipe_response.status_code != 200:
            print(f"Recipe API error: {recipe_response.text}")
            return {
                'weather': {
                    'temp': round(temp),
                    'condition': weather_condition,
                    'city': city_name
                },
                'message': recommendation['message'],
                'recipes': []
            }
            
        recipe_data = recipe_response.json()
        all_recipes = recipe_data.get("results", [])
        print(f"Found {len(all_recipes)} recipes")
        
        if not all_recipes:
            print("No recipes found in API response")
            return {
                'weather': {
                    'temp': round(temp),
                    'condition': weather_condition,
                    'city': city_name
                },
                'message': recommendation['message'],
                'recipes': []
            }
        
        # Select 3 random recipes
        selected_recipes = random.sample(all_recipes, min(3, len(all_recipes)))
        print(f"Selected {len(selected_recipes)} recipes")
        
        return {
            'weather': {
                'temp': round(temp),
                'condition': weather_condition,
                'city': city_name
            },
            'message': recommendation['message'],
            'recipes': selected_recipes
        }
        
    except Exception as e:
        print(f"Error in get_weather_recommendations: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

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
    Render the frontend page with weather-based recommendations
    """
    city = request.args.get('city', 'Jakarta')  # Default ke Jakarta jika tidak ada kota yang diinput
    weather_data = get_weather_recommendations(city)
    return render_template("index.html", weather_data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)


# Example usage of Spoonacular API
API_KEY = "your_spoonacular_api_key"
url = "https://api.spoonacular.com/recipes/complexSearch"
params = {
    "apiKey": API_KEY,
    "query": "pasta",
    "number": 1
}
response = requests.get(url, params=params)
print(f"Status: {response.status_code}")
print(response.json())
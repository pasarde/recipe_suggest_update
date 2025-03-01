<<<<<<< HEAD
# Recipe Suggestion App

A Flask-based web application that suggests recipes based on ingredients, weather conditions, and allows users to save their favorite recipes.

## Features

1. **Weather-Based Recipe Recommendations**
   - Displays current temperature and weather conditions for any city
   - Suggests recipes based on weather:
     - Rainy weather → Hot soups and warm dishes
     - Clear weather → Fresh salads and cold dishes
     - Cloudy weather → Comfort food and pasta dishes

2. **Ingredient-Based Recipe Search**
   - Search recipes by entering available ingredients
   - Results show:
     - Recipe title
     - Preparation time
     - Serving size
     - Recipe image
     - Detailed instructions

3. **Favorite Recipes**
   - Save recipes to favorites
   - View all favorite recipes in one place
   - Quick access to saved recipes

4. **Recipe Likes**
   - Like recipes you enjoy
   - Liked recipes appear first in search results
   - Helps personalize recommendations

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/desxtra/recipe_suggestions.git
   cd recipe_suggestions
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your API keys:
   ```plaintext
   SPOONACULAR_KEY="YOUR_SPOONACULAR_API_KEY"
   OPENWEATHER_KEY="YOUR_OPENWEATHER_API_KEY"
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Usage Guide

### Weather-Based Recommendations
1. Open the application in your browser
2. Default city is set to Jakarta
3. To change city:
   - Enter city name in the search box
   - Click "Cari" (Search)
4. View recommended recipes based on current weather

### Ingredient-Based Search
1. Scroll to the ingredient search form
2. Enter ingredients separated by commas (e.g., "tomato,basil,garlic")
3. Click "Search"
4. Browse through the recipe results

### Managing Favorites
1. Click "View Recipe" on any recipe card
2. In the recipe detail page:
   - Click "❤️ Add to Favorites" to save
   - Click "👍 Like" to like the recipe
3. Access favorites through "My Favorites" button

## API Requirements

- **Spoonacular API**: For recipe data
  - Get your key at: [Spoonacular API](https://spoonacular.com/food-api)
- **OpenWeather API**: For weather data
  - Get your key at: [OpenWeather](https://openweathermap.org/api)

## Technical Details

- Built with Flask (Python web framework)
- SQLite database for storing favorites and likes
- JavaScript for dynamic recipe loading
- Responsive design for mobile and desktop

## Troubleshooting

If recipes aren't displaying:
1. Check your API keys in `.env` file
2. Ensure you have internet connection
3. Check console for error messages
=======
# Recipe Suggestion App

A Flask-based web application that suggests recipes based on ingredients, weather conditions, and allows users to save their favorite recipes.

## Features

1. **Weather-Based Recipe Recommendations**
   - Displays current temperature and weather conditions for any city
   - Suggests recipes based on weather:
     - Rainy weather → Hot soups and warm dishes
     - Clear weather → Fresh salads and cold dishes
     - Cloudy weather → Comfort food and pasta dishes

2. **Ingredient-Based Recipe Search**
   - Search recipes by entering available ingredients
   - Results show:
     - Recipe title
     - Preparation time
     - Serving size
     - Recipe image
     - Detailed instructions

3. **Favorite Recipes**
   - Save recipes to favorites
   - View all favorite recipes in one place
   - Quick access to saved recipes

4. **Recipe Likes**
   - Like recipes you enjoy
   - Liked recipes appear first in search results
   - Helps personalize recommendations

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/desxtra/recipe_suggestions.git
   cd recipe_suggestions
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your API keys:
   ```plaintext
   SPOONACULAR_KEY="YOUR_SPOONACULAR_API_KEY"
   OPENWEATHER_KEY="YOUR_OPENWEATHER_API_KEY"
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Usage Guide

### Weather-Based Recommendations
1. Open the application in your browser
2. Default city is set to Jakarta
3. To change city:
   - Enter city name in the search box
   - Click "Cari" (Search)
4. View recommended recipes based on current weather

### Ingredient-Based Search
1. Scroll to the ingredient search form
2. Enter ingredients separated by commas (e.g., "tomato,basil,garlic")
3. Click "Search"
4. Browse through the recipe results

### Managing Favorites
1. Click "View Recipe" on any recipe card
2. In the recipe detail page:
   - Click "❤️ Add to Favorites" to save
   - Click "👍 Like" to like the recipe
3. Access favorites through "My Favorites" button

## API Requirements

- **Spoonacular API**: For recipe data
  - Get your key at: [Spoonacular API](https://spoonacular.com/food-api)
- **OpenWeather API**: For weather data
  - Get your key at: [OpenWeather](https://openweathermap.org/api)

## Technical Details

- Built with Flask (Python web framework)
- SQLite database for storing favorites and likes
- JavaScript for dynamic recipe loading
- Responsive design for mobile and desktop

## Troubleshooting

If recipes aren't displaying:
1. Check your API keys in `.env` file
2. Ensure you have internet connection
3. Check console for error messages
>>>>>>> 9c7f9b4f899f30276a81df47a089dbcf9bf44669
4. Verify API daily limits haven't been exceeded
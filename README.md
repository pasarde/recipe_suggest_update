# Recipe Suggestion App

This is the ML component of the Recipe Suggestion App. It uses TF-IDF to recommend recipes based on user-provided ingredients.

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

3. Add your Spoonacular API key to a .env file:

    - SPOONACULAR_KEY="YOUR_SPOONACULAR_API_KEY"

4. Run the App:
    ```bash
    python app.py
    ```
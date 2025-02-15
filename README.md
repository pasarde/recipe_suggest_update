# Recipe Suggestion App

This is the ML component of the Recipe Suggestion App. It uses TF-IDF to recommend recipes based on user-provided ingredients.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/desxtra/recipeRecommendations.git
   cd recipeRecommendations
   ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Add your Spoonacular API key to a .env file:
    ```bash
    SPOONACULAR_KEY="YOUR_SPOONACULAR_API_KEY"
    ```

4. Run the pipeline:
    - Fetch data: python src/data_fetching.py
    - Clean data: python src/preprocess.py
    - Train model: python src/train_model.py

5. Test recommendations:
    ```bash
    python tests/test_recommend.py
    ```
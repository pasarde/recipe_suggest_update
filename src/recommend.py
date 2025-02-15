import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# Load the pre-trained TF-IDF model and cleaned data
tfidf = joblib.load("models/tfidf_model.pkl")
df = pd.read_csv("data/processed/clean_recipes.csv")

# Convert ingredients to strings (for consistency)
df["ingredients_str"] = df["ingredients"].apply(", ".join)

# Precompute TF-IDF matrix for all recipes (do this ONCE here)
tfidf_matrix = tfidf.transform(df["ingredients_str"])

def recommend(user_ingredients):
    # 1. Preprocess user input
    user_input = ", ".join([ingredient.strip().lower() for ingredient in user_ingredients])
    
    # 2. Transform input using the TF-IDF model
    input_tfidf = tfidf.transform([user_input])
    
    # 3. Calculate similarity scores
    similarities = cosine_similarity(input_tfidf, tfidf_matrix)
    
    # 4. Add similarity scores to DataFrame
    df["similarity"] = similarities[0]
    
    # 5. Return top 5 recipes
    return df.sort_values("similarity", ascending=False).head(5)
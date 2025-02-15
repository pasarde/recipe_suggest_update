import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load cleaned data
df = pd.read_csv("data/processed/clean_recipes.csv")

# Convert ingredients to strings
df["ingredients_str"] = df["ingredients"].apply(", ".join)

# Train and save TF-IDF model
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["ingredients_str"])

joblib.dump(tfidf, "models/tfidf_model.pkl")
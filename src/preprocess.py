import pandas as pd

def clean_data():
    df = pd.read_csv("data/raw/recipes.csv")
    
    # Convert ingredients to lowercase lists
    df["ingredients"] = df["ingredients"].apply(
        lambda x: [ingredient.strip().lower() for ingredient in x.split(",")]
    )
    
    # Remove duplicates
    df = df.drop_duplicates(subset=["title"])
    
    df.to_csv("data/processed/clean_recipes.csv", index=False)
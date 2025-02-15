# tests/test_recommend.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommend import recommend

def test_recommend():
    # Test 1: Basic ingredients
    result = recommend(["tomato", "garlic"])
    assert not result.empty, "No recipes found for tomato + garlic"
    print("Test 1 Results (Tomato + Garlic):")
    print(result[["title", "ingredients", "similarity"]].head(2))

    # Test 2: No matching ingredients
    result = recommend(["unicorn tears"])
    assert not result.empty, "No recipes found for unicorn tears"
    print("\nTest 2 Results (No Matches):")
    print(result[["title", "ingredients", "similarity"]].head(2))
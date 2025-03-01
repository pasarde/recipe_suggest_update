import sqlite3

def init_db():
    """Initialize database with favorites and likes tables"""
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    # Create favorites table
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            recipe_id INTEGER PRIMARY KEY,
            title TEXT,
            image TEXT,
            ready_in_minutes INTEGER,
            servings INTEGER,
            instructions TEXT,
            ingredients TEXT
        )
    ''')
    
    # Create likes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            recipe_id INTEGER PRIMARY KEY,
            title TEXT,
            likes INTEGER DEFAULT 1,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_favorite(recipe_data):
    """Add a recipe to favorites"""
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO favorites 
        (recipe_id, title, image, ready_in_minutes, servings, instructions, ingredients)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        recipe_data['id'],
        recipe_data['title'],
        recipe_data['image'],
        recipe_data['readyInMinutes'],
        recipe_data['servings'],
        recipe_data['instructions'],
        ','.join([ing['original'] for ing in recipe_data['extendedIngredients']])
    ))
    conn.commit()
    conn.close()

def get_favorites():
    """Get all favorite recipes"""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    favorites = c.execute('SELECT * FROM favorites').fetchall()
    conn.close()
    return favorites

def add_like(recipe_data):
    """Add or update a recipe like"""
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO likes (recipe_id, title)
        VALUES (?, ?)
    ''', (recipe_data['id'], recipe_data['title']))
    conn.commit()
    conn.close()

def get_liked_recipes():
    """Get all liked recipes"""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    liked = c.execute('SELECT * FROM likes ORDER BY timestamp DESC').fetchall()
    conn.close()
    return liked

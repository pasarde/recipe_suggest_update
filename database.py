import sqlite3

def init_db():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            recipe_id INTEGER PRIMARY KEY,
            title TEXT,
            image TEXT,
            ready_in_minutes INTEGER,
            servings INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            recipe_id INTEGER PRIMARY KEY,
            title TEXT,
            likes INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()
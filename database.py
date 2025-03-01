<<<<<<< HEAD
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
=======
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
>>>>>>> 9c7f9b4f899f30276a81df47a089dbcf9bf44669
    conn.close()
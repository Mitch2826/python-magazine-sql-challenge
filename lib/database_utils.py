import sqlite3

DB_FILE = 'magazine.db'

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    # enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    #create authors table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL    
        )
    ''')
    
    #create magazines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    
    #create articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )
    ''')
    
    conn.commit()
    conn.close()
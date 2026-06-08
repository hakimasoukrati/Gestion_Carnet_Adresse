import sqlite3


def get_connection():
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telephone TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
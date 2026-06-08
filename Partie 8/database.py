import sqlite3
import os

DB_NAME = "contacts.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # =================================================
    # TABLE PRINCIPALE
    # =================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telephone TEXT NOT NULL
    )
    """)

    # =================================================
    # AJOUT DES NOUVELLES COLONNES (SAFE MIGRATION)
    # =================================================

    def add_column_if_not_exists(column_name, column_type):
        try:
            cursor.execute(f"ALTER TABLE contacts ADD COLUMN {column_name} {column_type}")
        except:
            pass  # colonne existe déjà

    add_column_if_not_exists("categorie", "TEXT")
    add_column_if_not_exists("adresse", "TEXT")
    add_column_if_not_exists("fonction", "TEXT")
    add_column_if_not_exists("entreprise", "TEXT")

    conn.commit()
    conn.close()


# =================================================
# RESET DB (OPTION UTILE POUR TESTS)
# =================================================
def reset_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    init_db() 
# CD-49: Mise a jour schema BDD 
 
# CD-50: Table categories en BDD 

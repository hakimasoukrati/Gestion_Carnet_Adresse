# database.py

import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("contacts.db",check_same_thread=False )
        self.cursor = self.conn.cursor()

        self.creer_tables()
    # -------------------------
    # CREATION DES TABLES
    # -------------------------
    def creer_tables(self):
        # TABLE CONTACTS
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telephone TEXT NOT NULL

        )
        """)

        # TABLE ADMINS
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL

        )
        """)

        self.conn.commit() 
# CD-32: Fonction get_all_contacts() depuis SQLite 
 
# CD-33: Fonction delete_contact() avec ID 
 
# CD-34: Fonction update_contact() pour modifier 

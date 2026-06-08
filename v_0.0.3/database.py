# database.py

import sqlite3


class Database:

    def __init__(self):

        self.conn = sqlite3.connect("contacts.db")
        self.cursor = self.conn.cursor()

        self.creer_tables()

    # -------------------------
    # CREATION DES TABLES
    # -------------------------
    def creer_tables(self):

        # Table contacts
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telephone TEXT NOT NULL

        )
        """)

        # Table admins
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL

        )
        """)

        self.conn.commit()
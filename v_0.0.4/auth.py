# auth.py

import hashlib
from database import Database


class Auth:

    db = Database()

    # -------------------------
    # HASH PASSWORD
    # -------------------------
    @staticmethod
    def hash_password(password):

        return hashlib.sha256(password.encode()).hexdigest()

    # -------------------------
    # CREER ADMIN
    # -------------------------
    @staticmethod
    def creer_admin():

        username = "admin"
        password = "1234"

        password_hash = Auth.hash_password(password)

        try:

            Auth.db.cursor.execute("""
            INSERT INTO admins(username, password)
            VALUES (?, ?)
            """, (username, password_hash))

            Auth.db.conn.commit()

        except:
            pass

    # -------------------------
    # LOGIN
    # -------------------------
    @staticmethod
    def verifier_login(username, password):

        password_hash = Auth.hash_password(password)

        Auth.db.cursor.execute("""
        SELECT *
        FROM admins
        WHERE username = ? AND password = ?
        """, (username, password_hash))

        user = Auth.db.cursor.fetchone()
        Auth.db.conn.close()
        return user is not None
        
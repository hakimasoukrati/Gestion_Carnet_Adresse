# auth.py

import hashlib
import os

FICHIER_USERS = "users.txt"


class Auth:

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def creer_admin():

        if not os.path.exists(FICHIER_USERS):

            with open(FICHIER_USERS, "w") as f:

                username = "admin"
                password = "1234"

                password_hash = Auth.hash_password(password)

                f.write(f"{username},{password_hash}\n")

    @staticmethod
    def verifier_login(username, password):

        if not os.path.exists(FICHIER_USERS):
            return False

        password_hash = Auth.hash_password(password)

        with open(FICHIER_USERS, "r") as f:

            for ligne in f:

                user, mdp = ligne.strip().split(",")

                if user == username and mdp == password_hash:
                    return True

        return False
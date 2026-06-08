# contact.py

import re


class Contact:

    def __init__(self, nom, email, telephone):

        self.nom = nom
        self.email = email
        self.telephone = telephone

        self.valider()

    # -------------------------
    # VALIDATION
    # -------------------------
    def valider(self):

        if not self.nom:
            raise ValueError("Le nom est obligatoire.")

        # Validation email
        pattern_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern_email, self.email):
            raise ValueError("Email invalide.")

        # Validation téléphone
        if not self.telephone.isdigit():
            raise ValueError("Téléphone invalide.")
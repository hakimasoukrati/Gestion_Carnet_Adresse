import re

class Contact:
    def __init__(self, nom, email, telephone):
        if not (isinstance(email, str) and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)):
            raise ValueError("Email invalid")

        if not (isinstance(nom, str) and nom.strip() != "" and re.match(r'^[A-Za-zÀ-ÿ\s]+$', nom)):
            raise ValueError("Nom invalide")
        if not (isinstance(telephone, str) and re.match(r'^(05|06|07)\d{8}$', telephone)):
            raise ValueError("Numéro marocain invalide")

        self.nom = nom
        self.email = email
        self.telephone = telephone

    def __str__(self):
        return f"{self.nom},{self.email},{self.telephone}"
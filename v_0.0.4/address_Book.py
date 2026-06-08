import csv

from database import Database
from contact import Contact


class AddressBook:

    def __init__(self):
        self.db = Database()

    # -------------------------
    # AJOUTER CONTACT
    # -------------------------
    def add_contact(self, contact):

        # Normalisation email
        email = contact.email.strip().lower()

        # Vérifier doublon (insensible à la casse)
        self.db.cursor.execute("""
        SELECT * FROM contacts WHERE LOWER(email) = ?
        """, (email,))

        exist = self.db.cursor.fetchone()

        if exist:
            return False

        # Insertion
        self.db.cursor.execute("""
        INSERT INTO contacts(nom, email, telephone)
        VALUES (?, ?, ?)
        """, (contact.nom, email, contact.telephone))

        self.db.conn.commit()

        return True

    # -------------------------
    # SUPPRIMER CONTACT
    # -------------------------
    def remove_contact(self, email):

        email = email.strip().lower()

        self.db.cursor.execute("""
        DELETE FROM contacts
        WHERE LOWER(email) = ?
        """, (email,))

        self.db.conn.commit()

    # -------------------------
    # RECUPERER CONTACTS
    # -------------------------
    def get_contacts(self):

        self.db.cursor.execute("""
        SELECT nom, email, telephone
        FROM contacts
        ORDER BY nom
        """)

        resultats = self.db.cursor.fetchall()

        contacts = []

        for nom, email, telephone in resultats:

            contacts.append(
                Contact(nom, email, telephone)
            )

        return contacts

    # -------------------------
    # AFFICHER CONTACTS (console)
    # -------------------------
    def display_contacts(self):

        contacts = self.get_contacts()

        for c in contacts:
            print(c.nom, c.email, c.telephone)

    # -------------------------
    # EXPORT CSV
    # -------------------------
    def export_csv(self):

        self.db.cursor.execute("""
        SELECT nom, email, telephone
        FROM contacts
        ORDER BY nom
        """)

        contacts = self.db.cursor.fetchall()

        with open("contacts.csv", "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow(["Nom", "Email", "Téléphone"])

            writer.writerows(contacts) 
# CD-32: Affichage des contacts recuperes 
 
# CD-33: Confirmation avant suppression 

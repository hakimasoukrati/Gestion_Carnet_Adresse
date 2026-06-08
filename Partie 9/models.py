import re
from database import get_connection


class ContactModel:

    # =================================================
    # VALIDATIONS
    # =================================================

    @staticmethod
    def is_valid_name(name):
        name = name.strip()
        return len(name) >= 2 and name.replace(" ", "").isalpha()

    @staticmethod
    def is_valid_email(email):
        email = email.strip()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_phone(phone):
        phone = phone.replace(" ", "").replace("-", "")

        # Maroc: 06/07 ou +212
        pattern = r"^(\+212|0)[5-7]\d{8}$"
        return re.match(pattern, phone) is not None


    # =================================================
    # AJOUT CONTACT
    # =================================================

    @staticmethod
    def add_contact(nom, email, telephone, categorie=None, adresse=None, fonction=None, entreprise=None):

        nom = nom.strip()
        email = email.strip().lower()
        telephone = telephone.strip()

        # VALIDATION
        if not ContactModel.is_valid_name(nom):
            return "invalid_name"

        if not ContactModel.is_valid_email(email):
            return "invalid_email"

        if not ContactModel.is_valid_phone(telephone):
            return "invalid_phone"

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO contacts
                (nom, email, telephone, categorie, adresse, fonction, entreprise)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nom, email, telephone, categorie, adresse, fonction, entreprise))

            conn.commit()
            return "success"

        except Exception as e:
            return str(e)

        finally:
            conn.close()


    # =================================================
    # AFFICHER CONTACTS
    # =================================================

    @staticmethod
    def get_all_contacts():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM contacts ORDER BY nom")
        contacts = cursor.fetchall()

        conn.close()
        return contacts


    # =================================================
    # SUPPRIMER CONTACT
    # =================================================

    @staticmethod
    def delete_contact(contact_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))

        conn.commit()
        conn.close()


    # =================================================
    # MODIFIER CONTACT
    # =================================================

    @staticmethod
    def update_contact(contact_id, nom, email, telephone,
                        categorie=None, adresse=None, fonction=None, entreprise=None):

        nom = nom.strip()
        email = email.strip().lower()
        telephone = telephone.strip()

        # VALIDATION
        if not ContactModel.is_valid_name(nom):
            return "invalid_name"

        if not ContactModel.is_valid_email(email):
            return "invalid_email"

        if not ContactModel.is_valid_phone(telephone):
            return "invalid_phone"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE contacts
            SET nom=?, email=?, telephone=?,
                categorie=?, adresse=?, fonction=?, entreprise=?
            WHERE id=?
        """, (nom, email, telephone,
              categorie, adresse, fonction, entreprise,
              contact_id))

        conn.commit()
        conn.close()

        return "success"


    # =================================================
    # RECHERCHE CONTACT
    # =================================================

    @staticmethod
    def search_contacts(query):

        if not query:
            return []

        query = query.lower()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM contacts
            WHERE LOWER(nom) LIKE ?
               OR LOWER(email) LIKE ?
               OR LOWER(categorie) LIKE ?
               OR LOWER(entreprise) LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))

        results = cursor.fetchall()
        conn.close()

        return results 
# CD-54: Modele RendezVous 
 
# CD-57: Tri par date des RDV 

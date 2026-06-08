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

        # Format Maroc : 06/07 + 8 chiffres ou +212...
        pattern = r"^(\+212|0)[5-7]\d{8}$"
        return re.match(pattern, phone) is not None


    # =================================================
    # AJOUT CONTACT
    # =================================================

    @staticmethod
    def add_contact(nom, email, telephone):

        nom = nom.strip()
        email = email.strip().lower()
        telephone = telephone.strip()

        # -------- VALIDATION --------
        if not ContactModel.is_valid_name(nom):
            return "invalid_name"

        if not ContactModel.is_valid_email(email):
            return "invalid_email"

        if not ContactModel.is_valid_phone(telephone):
            return "invalid_phone"

        # -------- DATABASE --------
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO contacts(nom, email, telephone)
                VALUES (?, ?, ?)
            """, (nom, email, telephone))

            conn.commit()
            return "success"

        except:
            return "error"

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
    def update_contact(contact_id, nom, email, telephone):

        nom = nom.strip()
        email = email.strip().lower()
        telephone = telephone.strip()

        # -------- VALIDATION --------
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
            SET nom=?, email=?, telephone=?
            WHERE id=?
        """, (nom, email, telephone, contact_id))

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
        """, (f"%{query}%", f"%{query}%"))

        results = cursor.fetchall()
        conn.close()

        return results 
# CD-37: Template index.html 
 
# CD-38: Template Jinja2 liste contacts 

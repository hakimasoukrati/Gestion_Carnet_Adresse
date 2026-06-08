import os
from contact import Contact

class AddressBook:

    def __init__(self, filename="contacts.txt"):
        self.filename = filename
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def add_contact(self, contact):
        contacts = self._load_contacts()

        for c in contacts:
            if c.email.strip() == contact.email.strip():
                print("Email déjà existant!")
                return

        with open(self.filename, "a") as f:
            f.write(str(contact) + "\n")

        print("Contact ajouté")

    def display_contacts(self):
        contacts = self._load_contacts()

        if not contacts:
            print("Aucun contact")
            return

        for c in contacts:
            print(c.nom, c.email, c.telephone)

    def remove_contact(self, email):
        contacts = self._load_contacts()

        found = False
        email = email.strip()
        new_contacts = []

        for c in contacts:
            if c.email.strip() == email:
                found = True
            else:
                new_contacts.append(c)

        with open(self.filename, "w") as f:
            for c in new_contacts:
                f.write(str(c) + "\n")

        if found:
            print("Contact supprimé")
        else:  
            print("Contact introuvable")
    def _load_contacts(self):
        contacts = []
        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip() 
                if line:
                    try:
                        nom, email, telephone = [x.strip() for x in line.split(",")]
                        contacts.append(Contact(nom, email, telephone))
                    except ValueError:
                        print("Ligne ignorée (donnée invalide)")

        return contacts
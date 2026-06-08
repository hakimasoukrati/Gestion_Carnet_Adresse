from contact import Contact
from address_Book import AddressBook
def main():
    carnet = AddressBook()

    while True:
        print("\n===== MENU =====")
        print("1. Ajouter un contact")
        print("2. Afficher les contacts")
        print("3. Supprimer un contact")
        print("4. Quitter")

        choix = input("Choix: ")

        try:
            if choix == "1":
                nom = input("Nom: ")
                email = input("Email: ")
                telephone = input("Téléphone: ")
                carnet.ajouter_contact(nom, email, telephone)

            elif choix == "2":
                carnet.afficher_contacts()

            elif choix == "3":
                nom = input("Nom du contact à supprimer: ")
                carnet.supprimer_contact(nom)

            elif choix == "4":
                print("Au revoir 👋")
                break
            else:
                print("Choix invalide.")
        except ValueError as e:
            print("Erreur:", e)

if __name__ == "__main__":
    main()
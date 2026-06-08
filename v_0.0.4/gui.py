# gui.py

import tkinter as tk
from tkinter import messagebox

from contact import Contact
from address_Book import AddressBook


class AddressBookGUI(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Allo !")
        self.geometry("520x500")
        self.resizable(False, False)

        self.carnet = AddressBook()

        self.contacts_affiches = []

        self.var_nom = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telephone = tk.StringVar()

        self.creer_frame_haut()
        self.creer_frame_milieu()
        self.creer_frame_bas()

        self.rafraichir_listbox()

    # -------------------------
    # FRAME HAUT
    # -------------------------
    def creer_frame_haut(self):

        self.frameH = tk.Frame(
            self,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )

        self.frameH.pack(fill="x", padx=8, pady=8)

        titre = tk.Label(
            self.frameH,
            text="Gestion des contacts",
            font=("Arial", 14, "bold")
        )

        titre.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 10)
        )

        tk.Label(
            self.frameH,
            text="Nom :"
        ).grid(row=1, column=0, sticky="w", pady=4)

        tk.Entry(
            self.frameH,
            textvariable=self.var_nom,
            width=35
        ).grid(row=1, column=1, pady=4)

        tk.Label(
            self.frameH,
            text="Email :"
        ).grid(row=2, column=0, sticky="w", pady=4)

        tk.Entry(
            self.frameH,
            textvariable=self.var_email,
            width=35
        ).grid(row=2, column=1, pady=4)

        tk.Label(
            self.frameH,
            text="Téléphone :"
        ).grid(row=3, column=0, sticky="w", pady=4)

        tk.Entry(
            self.frameH,
            textvariable=self.var_telephone,
            width=35
        ).grid(row=3, column=1, pady=4)

        tk.Button(
            self.frameH,
            text="Effacer",
            command=self.effacer_champs
        ).grid(row=4, column=0, columnspan=2, pady=(10, 0))

    # -------------------------
    # FRAME MILIEU
    # -------------------------
    def creer_frame_milieu(self):

        self.frameM = tk.Frame(
            self,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )

        self.frameM.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        self.listbox = tk.Listbox(
            self.frameM,
            height=12,
            width=55,
            exportselection=False
        )

        self.scrollbar = tk.Scrollbar(
            self.frameM,
            orient="vertical",
            command=self.listbox.yview
        )

        self.listbox.config(
            yscrollcommand=self.scrollbar.set
        )

        self.listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(side="right", fill="y")

        self.listbox.bind(
            "<<ListboxSelect>>",
            self.on_select
        )

    # -------------------------
    # FRAME BAS
    # -------------------------
    def creer_frame_bas(self):

        self.frameB = tk.Frame(
            self,
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )

        self.frameB.pack(fill="x", padx=8, pady=8)

        tk.Button(
            self.frameB,
            text="Ajouter",
            width=12,
            command=self.ajouter_contact
        ).pack(side="left", padx=5)

        tk.Button(
            self.frameB,
            text="Supprimer",
            width=12,
            command=self.supprimer_contact
        ).pack(side="left", padx=5)

        tk.Button(
            self.frameB,
            text="Afficher",
            width=12,
            command=self.afficher_contacts
        ).pack(side="left", padx=5)

        tk.Button(
            self.frameB,
            text="Exporter CSV",
            width=12,
            command=self.exporter_csv
        ).pack(side="left", padx=5)

    # -------------------------
    # OUTILS
    # -------------------------
    def effacer_champs(self):

        self.var_nom.set("")
        self.var_email.set("")
        self.var_telephone.set("")

        self.listbox.selection_clear(0, tk.END)

    def recuperer_contact_selectionne(self):

        selection = self.listbox.curselection()

        if not selection:
            return None

        index = selection[0]

        if 0 <= index < len(self.contacts_affiches):
            return self.contacts_affiches[index]

        return None

    def rafraichir_listbox(self):

        self.contacts_affiches = self.carnet.get_contacts()

        self.listbox.delete(0, tk.END)

        for contact in self.contacts_affiches:

            texte = f"{contact.nom} | {contact.email} | {contact.telephone}"

            self.listbox.insert(tk.END, texte)

    def on_select(self, event=None):

        contact = self.recuperer_contact_selectionne()

        if contact:

            self.var_nom.set(contact.nom)
            self.var_email.set(contact.email)
            self.var_telephone.set(contact.telephone)

    # -------------------------
    # ACTIONS
    # -------------------------
    def ajouter_contact(self):

        nom = self.var_nom.get().strip()
        email = self.var_email.get().strip()
        telephone = self.var_telephone.get().strip()

        try:

            contact = Contact(
                nom,
                email,
                telephone
            )

        except ValueError as e:

            messagebox.showerror(
                "Erreur",
                str(e)
            )

            return

        succes = self.carnet.add_contact(contact)

        if succes:

            self.rafraichir_listbox()

            messagebox.showinfo(
                "Succès",
                "Contact ajouté."
            )

            self.effacer_champs()

        else:

            messagebox.showwarning(
                "Attention",
                "Email déjà existant."
            )

    def supprimer_contact(self):

        contact = self.recuperer_contact_selectionne()

        if not contact:

            messagebox.showwarning(
                "Attention",
                "Sélectionnez un contact."
            )

            return

        self.carnet.remove_contact(contact.email)

        self.rafraichir_listbox()

        messagebox.showinfo(
            "Succès",
            "Contact supprimé."
        )

        self.effacer_champs()

    def afficher_contacts(self):

        self.rafraichir_listbox()

        if not self.contacts_affiches:

            messagebox.showinfo(
                "Contacts",
                "Aucun contact."
            )

            return

        texte = "\n".join(
            f"{c.nom} | {c.email} | {c.telephone}"
            for c in self.contacts_affiches
        )

        messagebox.showinfo(
            "Liste des contacts",
            texte
        )

    def exporter_csv(self):

        self.carnet.export_csv()

        messagebox.showinfo(
            "Succès",
            "Contacts exportés en CSV."
        )


if __name__ == "__main__":

    app = AddressBookGUI()
    app.mainloop()
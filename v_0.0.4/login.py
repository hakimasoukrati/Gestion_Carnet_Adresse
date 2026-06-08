# login.py

import tkinter as tk
from tkinter import messagebox

from auth import Auth
from gui import AddressBookGUI

Auth.creer_admin()
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion")
        self.geometry("350x250")
        self.resizable(False, False)

        titre = tk.Label(
            self,
            text="Authentification",
            font=("Arial", 16, "bold")
        )

        titre.pack(pady=20)

        tk.Label(
            self,
            text="Nom d'utilisateur"
        ).pack()

        self.entry_user = tk.Entry(self, width=30)
        self.entry_user.pack(pady=5)

        tk.Label(
            self,
            text="Mot de passe"
        ).pack()

        self.entry_pass = tk.Entry(
            self,
            show="*",
            width=30
        )

        self.entry_pass.pack(pady=5)

        btn_login = tk.Button(
            self,
            text="Se connecter",
            width=20,
            command=self.login
        )

        btn_login.pack(pady=20)

    def login(self):

        username = self.entry_user.get()
        password = self.entry_pass.get()

        if Auth.verifier_login(username, password):

            messagebox.showinfo(
                "Succès",
                "Connexion réussie"
            )

            self.destroy()

            app = AddressBookGUI()
            app.mainloop()

        else:

            messagebox.showerror(
                "Erreur",
                "Login incorrect"
            )
        def close(self):
            self.conn.close()


if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()
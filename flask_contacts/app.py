from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_connection
import models
print("MODELS OK")
from models import ContactModel

app = Flask(__name__)

init_db()

# -------------------------
# HOME (AFFICHER CONTACTS)
# -------------------------
@app.route("/")
def index():

    conn = get_connection()
    contacts = conn.execute("SELECT * FROM contacts ORDER BY nom").fetchall()
    conn.close()

    return render_template("index.html", contacts=contacts)


# -------------------------
# AJOUT CONTACT
# -------------------------
@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        nom = request.form["nom"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        result = ContactModel.add_contact(nom, email, telephone)

        if result != "success":
            return f"Erreur: {result}"

        return redirect(url_for("index"))

    return render_template("add.html")


# -------------------------
# SUPPRIMER CONTACT
# -------------------------
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_connection()

    conn.execute("DELETE FROM contacts WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# -------------------------
# MODIFIER CONTACT
# -------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = get_connection()
    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (id,)).fetchone()
    conn.close()

    if request.method == "POST":

        nom = request.form["nom"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        result = ContactModel.update_contact(id, nom, email, telephone)

        if result != "success":
            return f"Erreur: {result}"

        return redirect(url_for("index"))

    return render_template("edit.html", contact=contact)


# -------------------------
# SEARCH
# -------------------------
@app.route("/search")
def search():

    query = request.args.get("q")
    contacts = ContactModel.search_contacts(query)

    return render_template("index.html", contacts=contacts)


if __name__ == "__main__":
    app.run(debug=True) 
# CD-36: Initialisation projet Flask 
 
# CD-36: Configuration de base de Flask 

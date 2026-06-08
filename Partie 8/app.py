from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import urllib.parse

from database import init_db, get_connection
from models import ContactModel

app = Flask(__name__)

init_db()

# =================================================
# EMAIL CONFIG
# =================================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mariaelmrabet555@gmail.com'
app.config['MAIL_PASSWORD'] = 'ozuw jnyf qoga nhxk'
app.config['MAIL_DEFAULT_SENDER'] = 'mariaelmrabet555@gmail.com'

mail = Mail(app)


# =================================================
# HOME
# =================================================
@app.route("/")
def index():
    contacts = ContactModel.get_all_contacts()
    return render_template("index.html", contacts=contacts)


# =================================================
# ADD CONTACT
# =================================================
@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        nom = request.form["nom"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        categorie = request.form.get("categorie")
        adresse = request.form.get("adresse")
        fonction = request.form.get("fonction")
        entreprise = request.form.get("entreprise")

        result = ContactModel.add_contact(
            nom, email, telephone,
            categorie, adresse, fonction, entreprise
        )

        if result != "success":
            return f"Erreur: {result}"

        return redirect(url_for("index"))

    return render_template("add.html")


# =================================================
# DELETE CONTACT
# =================================================
@app.route("/delete/<int:id>")
def delete(id):
    ContactModel.delete_contact(id)
    return redirect(url_for("index"))


# =================================================
# EDIT CONTACT
# =================================================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if request.method == "POST":

        nom = request.form["nom"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        categorie = request.form.get("categorie")
        adresse = request.form.get("adresse")
        fonction = request.form.get("fonction")
        entreprise = request.form.get("entreprise")

        result = ContactModel.update_contact(
            id, nom, email, telephone,
            categorie, adresse, fonction, entreprise
        )

        if result != "success":
            return f"Erreur: {result}"

        return redirect(url_for("index"))

    conn = get_connection()
    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("edit.html", contact=contact)


# =================================================
# SEARCH
# =================================================
@app.route("/search")
def search():
    query = request.args.get("q", "")
    contacts = ContactModel.search_contacts(query)
    return render_template("index.html", contacts=contacts)


# =================================================
# SEND EMAIL
# =================================================
@app.route("/send_email/<int:id>")
def send_email(id):

    conn = get_connection()
    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (id,)).fetchone()
    conn.close()

    if not contact:
        return "Contact introuvable"

    try:
        msg = Message(
            subject="Message depuis l'application Flask",
            recipients=[contact["email"]],
            body=f"""
Bonjour {contact['nom']},

Votre contact est bien enregistré dans notre système.

Cordialement,
Gestion des contacts
"""
        )

        mail.send(msg)
        return "Email envoyé avec succès ✅"

    except Exception as e:
        return f"Erreur email: {str(e)}"


# =================================================
# SEND WHATSAPP
# =================================================
@app.route("/send_whatsapp/<int:id>")
def send_whatsapp(id):

    conn = get_connection()
    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (id,)).fetchone()
    conn.close()

    if not contact:
        return "Contact introuvable"

    phone = contact["telephone"].strip()

    phone = phone.replace("+", "").replace(" ", "").replace("-", "")

    if phone.startswith("0"):
        phone = "212" + phone[1:]

    if not phone.isdigit():
        return "Numéro invalide"

    message = f"""
Bonjour {contact['nom']},

Message envoyé depuis l'application de gestion des contacts.

Cordialement,
Système CRM
"""

    url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"

    return redirect(url)


# =================================================
# RUN
# =================================================
if __name__ == "__main__":
    app.run(debug=True) 
# CD-51: Selection categorie lors ajout contact 
 
# CD-52: Menu deroulant filtre par categorie 

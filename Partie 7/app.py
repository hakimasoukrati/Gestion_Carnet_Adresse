from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import urllib.parse

from database import init_db, get_connection
from models import ContactModel

app = Flask(__name__)

init_db()

# =================================================
# CONFIG EMAIL (GMAIL)
# =================================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mariaelmrabet555@gmail.com'
app.config['MAIL_PASSWORD'] = 'ozuw jnyf qoga nhxk'   # ⚠️ ne jamais mettre mot de passe normal
app.config['MAIL_DEFAULT_SENDER'] = 'mariaelmrabet555@gmail.com'

mail = Mail(app)


# =================================================
# HOME
# =================================================
@app.route("/")
def index():

    conn = get_connection()
    contacts = conn.execute("SELECT * FROM contacts ORDER BY nom").fetchall()
    conn.close()

    return render_template("index.html", contacts=contacts)


# =================================================
# AJOUT CONTACT
# =================================================
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


# =================================================
# SUPPRIMER CONTACT
# =================================================
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_connection()
    conn.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# =================================================
# MODIFIER CONTACT
# =================================================
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


# =================================================
# SEARCH
# =================================================
@app.route("/search")
def search():

    query = request.args.get("q")
    contacts = ContactModel.search_contacts(query)

    return render_template("index.html", contacts=contacts)


# =================================================
# ENVOI EMAIL
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

Nous vous contactons via notre application de gestion des contacts.

Votre dossier a été mis à jour avec succès.

Cordialement,
Team Application Flask
"""
        )

        mail.send(msg)
        return "Email envoyé avec succès ✅"

    except Exception as e:
        return f"Erreur email: {str(e)}"


# =================================================
# ENVOI WHATSAPP
# =================================================
@app.route("/send_whatsapp/<int:id>")
def send_whatsapp(id):

    conn = get_connection()
    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (id,)).fetchone()
    conn.close()

    if not contact:
        return "Contact introuvable"

    phone = contact["telephone"].strip()

    # Nettoyage
    phone = phone.replace("+", "").replace(" ", "").replace("-", "")

    # Conversion Maroc
    if phone.startswith("0"):
        phone = "212" + phone[1:]

    if not phone.isdigit():
        return "Numéro invalide"

    message = f"""
Bonjour {contact['nom']},

Nous vous contactons depuis notre application de gestion de carnet de contacts.

Cordialement,
Service de gestion des contacts
"""
    url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"

    return redirect(url)


# =================================================
# RUN APP
# =================================================
if __name__ == "__main__":
    app.run(debug=True) 
# CD-43: Configuration SMTP pour envoi emails 
 
# CD-44: Fonction send_email() avec smtplib 
 
# CD-44: Interface pour saisir sujet et message 
 
# CD-46: Integration API WhatsApp avec pywhatkit 
 
# CD-47: Fonction send_whatsapp(numero, message) 
 
# CD-47: Bouton WhatsApp dans interface 

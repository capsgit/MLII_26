import sqlite3
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
DB_PATH = Path(__file__).resolve().parent / "guest_book.db"

# ---------------------------------------------------------------
# -----------------------------DB--------------------------------
# ---------------------------------------------------------------

def datenbank_erstellen():
    with sqlite3.connect("guest_book.db") as conn:
        c = conn.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS guest_book (
            id INTEGER PRIMARY KEY,
            name TEXT,
            surename TEXT,
            gender TEXT,
            wishes TEXT,
            e_mail TEXT,
            prefix TEXT,
            phone_number TEXT,
            date TEXT,
            message TEXT
        )
        """
        c.execute(sql)
        conn.commit()


# ---------------------------------------------------------------
# ------------------------app routen-----------------------------
# ---------------------------------------------------------------

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/guest_book", methods=["GET", "POST"])
def guest_book():
    wishes = []
    if request.method == "POST":
        name = request.form["name"]
        surename = request.form["surename"]
        e_mail = request.form["email"]
        phone_prefix = request.form["prefix"]
        phone_number = request.form["number"]
        date = request.form["date"]
        wishes = request.form.getlist("wishes")
        gender = request.form["gender"]
        message = request.form["message"]

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()

            wishes_list = ", ".join(wishes)

            c.execute("""
                      INSERT INTO guest_book (name, surename, gender, wishes, e_mail, prefix, phone_number, date, message)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                      """, (name, surename, gender, wishes_list, e_mail, phone_prefix, phone_number, date, message))
            conn.commit()

        return "Guardado en la DB ✅ ---> La informacion ha sido enviada."
    return render_template("index.html", wishes=wishes)


if __name__ == "__main__":
    datenbank_erstellen()
    app.run(debug=True)

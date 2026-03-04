from flask import Flask, render_template, redirect, url_for, request, flash
import os

app = Flask(__name__)
# llamamos a UPLOAD de flask y lo definimos como "uploads/"
# aca se van a guardar los archivos subidos
app.config["UPLOAD_FOLDER"] = "uploads/"
app.secret_key = "supersecretkey" # en principio no es necesario complejisar la llave

DATAPATH = "data.txt" # aca llegara el contenido del archivo

@app.route('/')
def index():
    return render_template('home.html')


@app.route("/products", methods=["GET", "POST"])
def products():
    product_list = [
        {"name": "Laptop", "price": 1000},
        {"name": "Smartphone", "price": 800},
        {"name": "Tablet", "price": 600},
    ]

    return render_template("products.html", products=product_list)

"""@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        neu_content = request.form["inhalt"]

        with open(DATAPATH, "w", encoding="UTF-8") as file:
            file.write(neu_content)

        flash("Data saved successfully!")


        # aca se asocia con la ruta, no al "url" sino a la funcion
        # no a "/mixed" sino a "form_mixed"
        return redirect(url_for("index"))

    try:
        with open (DATAPATH, "r", encoding="utf-8") as file:
            content = file.read().strip()
    except FileNotFoundError:
        content = ""
    return render_template("edit.html", inhalt=content)
"""
@app.route("/mixed", methods = ["GET","POST"])
def form_mixed():
    # leer los datos desde el formlario
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        skills = request.form.getlist("skills")
        resume = request.files["resume"]

        # guardar el archivo
        resume.save(os.path.join(app.config["UPLOAD_FOLDER"], resume.filename))
        return render_template("result.html",
                               name=name,
                               age=age,
                               gender=gender,
                               skills=skills,
                               filename= resume.filename)
    return render_template("form_mixed.html")

@app.route("/upload", methods = ["GET","POST"])
def form_upload():
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

        return f"Datei {file.filename} erfolgreich hochgeladen!"
    return render_template("form_upload.html")

@app.route("/form_checkboxes", methods=["GET", "POST"])
def form_checkboxes():
    message = None
    skills = []

    if request.method == "POST":
        skills = request.form.getlist("skills")

        if not skills:
            message = "Keine Auswahl"
        elif len(skills) == 1:
            message = f"Ausgewählte Fähigkeit: {', '.join(skills)}"
        else:
            message = f"Ausgewählte Fähigkeiten: {', '.join(skills)}"

    return render_template("form_checkboxes.html", skills=skills, message=message)
    #return f"Hallo Welt {name}!"

@app.route("/form_options", methods=["GET"])
def form_options():
    selected_dropdown = None
    selected_radio = None

    if request.method == "POST":
        return render_template("form_options.html",
                               selected_dropdown=selected_dropdown, selected_radio=selected_radio)

if __name__ == "__main__":
    app.run(debug=True)
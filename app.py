from flask import Flask, request, render_template
app = Flask(__name__)
@app.route("/")

def home():
    return "Hola bienvenidos campistas a mi aplicación"

@app.route("/inicio/")

def inicio():
    return render_template("index.html")

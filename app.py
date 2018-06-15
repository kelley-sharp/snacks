from flask import Flask, request, url_for, render_template
from flask_modus import Modus

app = Flask(__name__)
modus = Modus(app)


class Snack:
    def __init__(self, id, name, kind):
        self.id = id
        self.name = name
        self.kind = kind


chocolate = Snack("1", "Chocolate", "Sweet")
popcorn = Snack("2", "Popcorn", "Salty")
soda = Snack("3", "Soda", "Sweet")

snacks = [chocolate, popcorn, soda]


@app.route("/snacks", methods=["GET"])
def display_snacks():
    return render_template("snacks.html", snacks=snacks)


@app.route("/form", methods=["GET"])
def show_form():
    return render_template("form.html")


@app.route("/snacks", methods=["PUT"])
def add_new_snack():
    snack_name = request.values.get("name")
    snack_kind = request.values.get("kind")

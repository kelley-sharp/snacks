from flask import Flask, request, url_for, render_template, redirect
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
snack_id = 1


@app.route("/snacks", methods=["GET"])
def display_snacks():
    return render_template("snacks.html", snacks=snacks)


@app.route("/form", methods=["GET"])
def show_form():
    return render_template("form.html")


@app.route("/snack", methods=["GET"])
def show_snack():
    return render_template("snack.html")


@app.route("/form", methods=["PUT"])
def add_new_snack():
    global snack_id
    new_snack = Snack(
        id=snack_id, name=request.form["name"], kind=request.form["kind"])
    snacks.append(new_snack)
    snack_id += 1
    return redirect(url_for("display_snacks"))

from flask import Flask, request, url_for, render_template, redirect
from flask_modus import Modus

app = Flask(__name__)
modus = Modus(app)


class Snack:
    def __init__(self, snack_id, name, kind):
        self.id = snack_id
        self.name = name
        self.kind = kind


chocolate = Snack(1, "Chocolate", "Sweet")
popcorn = Snack(2, "Popcorn", "Salty")
soda = Snack(3, "Soda", "Sweet")

snacks = [chocolate, popcorn, soda]
snack_id = 4


@app.route("/snacks", methods=["GET"])
def display_snacks():
    return render_template("snacks.html", snacks=snacks)


@app.route("/form", methods=["GET"])
def show_form():
    return render_template("form.html")


@app.route("/snacks/<int:id>", methods=["GET"])
def show_snack(id):

    found_snack = [snack for snack in snacks if snack.id == id][0]
    return render_template("snack.html", snack=found_snack)


@app.route("/form", methods=["PUT"])
def add_new_snack():
    global snack_id
    new_snack = Snack(
        snack_id=snack_id,
        name=request.form["name"],
        kind=request.form["kind"])
    snacks.append(new_snack)
    snack_id += 1
    return redirect(url_for("display_snacks"))


@app.route("/snacks/<int:id>", methods=["DELETE"])
def remove_snack(id):
    global snack_id
    found_snack = [snack for snack in snacks if snack.id == id][0]
    snacks.remove(found_snack)
    return redirect(url_for("display_snacks"))


@app.route("/snacks/<int:id>/edit", methods=["GET"])
def edit_snack(id):
    global snack_id
    found_snack = [snack for snack in snacks if snack.id == id][0]
    return render_template("edit.html", snack=found_snack)


@app.route("/snacks/<int:id>", methods=["PATCH"])
def update_snack(id):
    found_snack = [snack for snack in snacks if snack.id == id][0]
    found_snack.name = request.form['name']
    found_snack.kind = request.form['kind']
    return redirect(url_for("show_snack", id=found_snack.id))

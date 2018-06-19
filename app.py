from flask import Flask, request, url_for, render_template, redirect
from flask_modus import Modus
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import psycopg2

DB = "postgresql://localhost/snacks"

app = Flask(__name__)
modus = Modus(app)
app.config['SECRET_KEY'] = "abc123"
toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Snack(db.Model):
    __tablename__ = "snacks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    kind = db.Column(db.Text)


db.create_all()


@app.route("/snacks", methods=["GET"])
def display_snacks():
    snacks = Snack.query.all()  # [<Snack>, <Snack>]
    return render_template("snacks.html", snacks=snacks)


@app.route("/form", methods=["GET"])
def show_form():
    return render_template("form.html")


@app.route("/snacks/<int:id>")
def show_snack(id):

    snack = Snack.query.filter(Snack.id == id).one()  # <Snack>
    return render_template("snack.html", snack=snack)


# @app.route("/snacks/<int:id>", methods=["GET"])
# def show_snack(id):

# found_snack = [snack for snack in snacks if snack.id == id][0]
# return render_template("snack.html", snack=found_snack)


@app.route("/form", methods=["PUT"])
def add_new_snack():
    name = request.values.get("name")
    kind = request.values.get("kind")

    new_snack = Snack(name=name, kind=kind)
    db.session.add(new_snack)
    db.session.commit()

    return redirect(url_for('display_snacks'))


@app.route("/snacks/<int:id>", methods=["DELETE"])
def remove_snack(id):

    snack = Snack.query.filter(Snack.id == id).one()
    db.session.delete(snack)
    db.session.commit()
    return redirect(url_for("display_snacks"))


@app.route("/snacks/<int:id>/edit", methods=["GET"])
def edit_snack(id):

    snack = Snack.query.filter(Snack.id == id).one()
    return render_template("edit.html", snack=snack)


@app.route("/snacks/<int:id>", methods=["PATCH"])
def update_snack(id):

    name = request.values.get("name")
    kind = request.values.get("kind")

    snack = Snack.query.filter(Snack.id == id).one()
    snack.name = name
    snack.kind = kind
    db.session.commit()
    return redirect(url_for("show_snack", id=snack.id))


#     from flask import Flask, request, url_for, render_template, redirect
# from flask_modus import Modus

# app = Flask(__name__)
# modus = Modus(app)

# class Snack:
#     def __init__(self, snack_id, name, kind):
#         self.id = snack_id
#         self.name = name
#         self.kind = kind

# chocolate = Snack(1, "Chocolate", "Sweet")
# popcorn = Snack(2, "Popcorn", "Salty")
# soda = Snack(3, "Soda", "Sweet")

# snacks = [chocolate, popcorn, soda]
# snack_id = 4

# @app.route("/snacks", methods=["GET"])
# def display_snacks():
#     return render_template("snacks.html", snacks=snacks)

# @app.route("/form", methods=["GET"])
# def show_form():
#     return render_template("form.html")

# @app.route("/snacks/<int:id>", methods=["GET"])
# def show_snack(id):

#     found_snack = [snack for snack in snacks if snack.id == id][0]
#     return render_template("snack.html", snack=found_snack)

# @app.route("/form", methods=["PUT"])
# def add_new_snack():
#     global snack_id
#     new_snack = Snack(
#         snack_id=snack_id,
#         name=request.form["name"],
#         kind=request.form["kind"])
#     snacks.append(new_snack)
#     snack_id += 1
#     return redirect(url_for("display_snacks"))

# @app.route("/snacks/<int:id>", methods=["DELETE"])
# def remove_snack(id):
#     global snack_id
#     found_snack = [snack for snack in snacks if snack.id == id][0]
#     snacks.remove(found_snack)
#     return redirect(url_for("display_snacks"))

# @app.route("/snacks/<int:id>/edit", methods=["GET"])
# def edit_snack(id):
#     global snack_id
#     found_snack = [snack for snack in snacks if snack.id == id][0]
#     return render_template("edit.html", snack=found_snack)

# @app.route("/snacks/<int:id>", methods=["PATCH"])
# def update_snack(id):
#     found_snack = [snack for snack in snacks if snack.id == id][0]
#     found_snack.name = request.form['name']
#     found_snack.kind = request.form['kind']
#     return redirect(url_for("show_snack", id=found_snack.id))

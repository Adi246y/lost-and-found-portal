from flask import Blueprint, render_template, request, redirect, session
from models.item import Item
from models.database import db
import os

items = Blueprint('items', __name__)

@items.route("/report", methods=["GET", "POST"])
def report():
    if 'user_id' not in session:
        return redirect("/login")

    if request.method == "POST":

        file = request.files['image']
        filename = file.filename

        if filename != "":
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
        else:
            filename = ""

        item = Item(
            title=request.form['title'],
            description=request.form['description'],
            category=request.form['category'],
            status=request.form['status'],
            location=request.form['location'],
            date=request.form['date'],
            image=filename,
            user_id=session['user_id']
        )

        db.session.add(item)
        db.session.commit()

        return redirect("/items")

    return render_template("report.html")


@items.route("/items")
def view_items():
    all_items = Item.query.all()
    return render_template("items.html", items=all_items)
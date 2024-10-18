from flask import Flask, g, render_template, request
import sqlite3
import os

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("db.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def main_page():
    return render_template("base.html")


@app.route("/books", methods=["GET", "POST"])
def get_books():
    print(request.method)
    if request.method == "GET":
        db = get_db()
        books = db.execute("SELECT * FROM book").fetchall()
        return render_template("books.html", books=books)
    if request.method == "POST":
        db = get_db()
        isbn = request.form["isbn"]
        author = request.form["author"]
        title = request.form["title"]
        year = request.form["year"]
        publisher = request.form["publisher"]
        db.execute(
            "INSERT INTO book (isbn, author, title, year, publisher, rented) VALUES (?, ?, ?, ?, ?, ?)",
            (isbn, author, title, year, publisher, False),
        )
        return render_template(request.referrer)
    return render_template("base.html")


if __name__ == "__main__":
    app.teardown_appcontext(close_db)
    app.run(debug=True)

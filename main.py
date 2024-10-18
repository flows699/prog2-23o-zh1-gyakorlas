from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

print(os.listdir("templates"))


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


@app.route("/members", methods=["GET", "POST"])
def show_members():
    db = get_db()
    error = None
    if request.method == "POST":
        name = request.form["name"]
        neptun = request.form["neptun"]
        try:
            db.execute(
                "INSERT INTO user (neptun, name, rentedbooks) VALUES (?, ?, ?)",
                (neptun, name, 0),
            )
            db.commit()
        except sqlite3.IntegrityError:
            error = f"The Neptun code '{neptun}' is already taken."

    members = db.execute("SELECT name, neptun FROM user").fetchall()
    return render_template("members.html", members=members, error=error)


@app.route("/books", methods=["GET", "POST"])
def get_books():
    if request.method == "GET":
        db = get_db()
        books = db.execute("SELECT * FROM book").fetchall()
        members = db.execute("SELECT name, neptun FROM user").fetchall()
        return render_template("books.html", books=books, members=members)
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
        db.commit()
        return redirect(url_for("get_books"))

    return render_template("base.html ")


@app.route("/checkout", methods=["POST"])
def checkout():
    bookid = request.form["id"]
    neptun = request.form["neptun"]

    db = get_db()

    book = db.execute("SELECT * FROM book WHERE id = ?", (bookid,)).fetchone()
    if book and book["rented"]:
        return redirect(url_for("get_books", error="A könyv már ki van kölcsönözve."))

    db.execute(
        "UPDATE book SET rented = True, rentcount = rentcount + 1, rented_by = ? WHERE id = ?",
        (neptun, bookid),
    )

    db.execute(
        "UPDATE user SET rentedbooks = rentedbooks + 1 WHERE neptun = ?", (neptun,)
    )

    db.commit()

    return redirect(url_for("get_books"))


@app.route("/return", methods=["POST"])
def return_book():
    bookid = request.form["id"]
    neptun = request.form["neptun"]

    db = get_db()

    db.execute(
        "UPDATE book SET rented = False, rented_by = NULL WHERE id = ?",
        (bookid,),
    )

    db.commit()
    return redirect(url_for("get_books"))


@app.route("/stats")
def stats():
    os.makedirs("static/images", exist_ok=True)
    db = get_db()

    books_checkout = db.execute(
        "SELECT title, rentcount FROM book WHERE rentcount > 0"
    ).fetchall()

    members_checkout = db.execute(
        "SELECT name, rentedbooks FROM user WHERE rentedbooks > 0"
    ).fetchall()

    book_titles = [book["title"] for book in books_checkout]
    book_counts = [book["rentcount"] for book in books_checkout]

    plt.bar(book_titles, book_counts, color="blue")
    plt.title("Number of times each book has been checked out")
    plt.xlabel("Book Title")
    plt.ylabel("Checkout Count")
    plt.savefig("static/images/book_checkout_stats.png")
    plt.close()

    member_names = [member["name"] for member in members_checkout]
    member_counts = [member["rentedbooks"] for member in members_checkout]

    plt.bar(member_names, member_counts, color="green")
    plt.title("Number of books checked out by each member")
    plt.xlabel("Member Name")
    plt.ylabel("Checkout Count")
    plt.savefig("static/images/member_checkout_stats.png")
    plt.close()

    return render_template("stats.html")


if __name__ == "__main__":
    app.teardown_appcontext(close_db)
    app.run(debug=True)

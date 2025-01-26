from .models import get_db_connection
from flask_session import Session
from flask import Blueprint, Flask, flash, redirect, render_template, request, session, current_app, url_for
from .utils import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
import random
from . import create_app
from .config import import_csv_to_db, import_recipes_to_db

## CREATE TABLE words ( id INT AUTO_INCREMENT PRIMARY KEY, georgian VARCHAR(100) NOT NULL, english VARCHAR(100) NOT NULL, ipa VARCHAR(100),
# category VARCHAR(50), added_date DATE DEFAULT CURRENT_DATE, difficulty_level INT DEFAULT 1, times_reviewed INT DEFAULT 0, last_reviewed DATE);

## CREATE TABLE recipes (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT NOT NULL, ingredients TEXT NOT NULL, instructions TEXT,
# category VARCHAR(100), image_url VARCHAR(255), added_date DATE DEFAULT CURRENT_DATE, difficulty_level INT DEFAULT 1,
# preparation_time VARCHAR(50), cooking_time VARCHAR(50));

## CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100) NOT NULL, email VARCHAR(255) NOT NULL,
# password VARCHAR(255) NOT NULL, date_joined DATE DEFAULT CURRENT_DATE, last_login DATETIME, profile_picture VARCHAR(255),
# preferred_language VARCHAR(10), points INT DEFAULT 1, current_level int default 1);

main = Blueprint("main", __name__, template_folder='../templates', static_folder="../static")

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/flashcards", methods=["GET", "POST"])

def flashcards():
    #__init__ function
    create_app
    ##importing words from CSV to DB file
    import_csv_to_db()

    if "username" not in session:
        flash("You must log in first", "warning")
        return redirect("/login")

    db = current_app.db

    level = db.execute("SELECT current_level FROM users WHERE username = ?", session["username"],)
    current_level = level[0]["current_level"]

    next_level = current_level + 1
    next_word = db.execute("SELECT georgian FROM words WHERE id = ?", next_level)

    word = db.execute("SELECT georgian FROM words WHERE id = ?", current_level)
    current_word = word[0]["georgian"]

    word_english = db.execute("SELECT english FROM words WHERE id = ?", current_level)
    current_english_word = word_english[0]["english"]

    word_ipa = db.execute("SELECT ipa FROM words WHERE id = ?", current_level)
    current_ipa_word = word_ipa[0]["ipa"]

    result = db.execute("SELECT MAX(id) AS highest_id FROM words")
    highest_id = result[0]["highest_id"]
    percentage = highest_id * (current_level/100)
    rounded = round(percentage)


    #fetching all words in database using .fetchall()
    all_words = db.execute("SELECT id, english FROM words")
    word_georgian = [word["english"] for word in all_words]
    word_id = [id["id"] for id in all_words]
    #checking if there is words at all
    if len(all_words) <= 1:
        flash("Not enough words in the database to generate options!", "warning")
        return redirect("/")

    incorrect_answers = random.sample([w for w in word_georgian if word_id != current_level], min(3, len(word_georgian) - 1))
    options = incorrect_answers + [current_english_word]
    random.shuffle(options)

    #declaring method and request for user and correct answer variables
    if request.method == "POST":
        user_answer = request.form.get("answer")
        current_word = request.form.get("correct_answer")
        points = db.execute("SELECT points FROM users WHERE username = ?", session["username"])
        tot_points = points[0]["points"]

        if user_answer == current_word:
            db.execute("UPDATE users SET points = points + 1 WHERE username = ?", session["username"])
            db.execute("UPDATE users SET current_level = current_level + 1 WHERE username = ?", session["username"])
            flash("Correct!", "success")
            if not next_word:
                db.execute("UPDATE users SET current_level = 1 WHERE username = ?", session["username"])
                flash("No more words!", "warning")
        else:
            if tot_points > 0:
                db.execute("UPDATE users SET points = points - 1 WHERE username = ?", session["username"])
            flash("Incorrect", "danger")
        return redirect("/flashcards")

    return render_template("flashcards.html", current_word=current_word, options=options, current_english_word=current_english_word, current_ipa_word=current_ipa_word, rounded=rounded)

@main.route('/reset', methods=['POST'])
def reset_level():
    db = current_app.db
    db.execute("UPDATE users SET current_level = 1 WHERE username = ?", (session["username"],))
    db.execute("UPDATE users SET points = 0 WHERE username = ?", (session["username"],))
    flash("Level and point reset successfully!", "success")
    return redirect("flashcards")

@main.route('/flip/<int:word_id>')
def flip(word_id):
    # Connect to the database
    conn = SQL("sqlite:///database.db")
    cursor = conn.cursor()

    # Fetch the word data
    cursor.execute("SELECT georgian, english, ipa, category FROM words WHERE id = ?", (word_id,))
    word = cursor.fetchone()

    # Close the connection
    conn.close()

    return render_template('flipcard.html', word=word)

@main.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()
    db = current_app.db

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        return redirect("/")

    else:
        return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")

@main.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    db = current_app.db

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("email"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords should not mismatch", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("username already taken", 400)

        db.execute("INSERT INTO users (username, email, password) VALUES(?, ?, ?)", request.form.get("username"), request.form.get("email"), generate_password_hash(request.form.get("password")))
        return redirect("/")
    else:
        return render_template("register.html")

@main.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        flash("You must log in first", "warning")
        return redirect("/login")
    db = current_app.db
    print((session["username"],))
    user = db.execute("SELECT * FROM users WHERE username = ?", (session["username"],))
    username = user[0]["username"]
    password = user[0]["password"]
    email = user[0]["email"]
    points = user[0]["points"]
    current_level = user[0]["current_level"]

    if request.method == "POST":
        change_user = request.form.get("username")
        change_email = request.form.get("email")
        old_password = request.form.get("old_password")
        change_password = request.form.get("new_password")
        repeat_password = request.form.get("repeat_password")
        if change_user:
            db.execute("UPDATE users SET username = ? WHERE username = ?", change_user, (session["username"],))
            session["username"] = change_user
            return redirect("/profile")
        elif change_email:
            db.execute("UPDATE users SET email = ? WHERE username = ?", change_email, (session["username"],))
            return redirect("/profile")
        elif old_password:
            if check_password_hash(password, old_password):
                if repeat_password == change_password:
                    db.execute("UPDATE users SET password = ? WHERE username = ?", generate_password_hash(change_password), (session["username"],))
                    flash("Password changed!", "success")
                    return redirect("/profile")
                else:
                    flash("New Password do not match!", "warning")
            else:
                flash("Old Password is incorrect!", "warning")
                return redirect("/profile")


    return render_template("profile.html", username=username, password=password, email=email, points=points, current_level=current_level)

@main.route("/recipe", methods=["GET", "POST"])
def recipe():
    import_recipes_to_db()
    db = current_app.db
    id = int(request.form.get("id", 1))

    if request.method == "POST":
        direction = request.form.get("direction")
        if direction == "prev_recipe":
            id -= 1
        elif direction == "next_recipe":
            id += 1

    recipes = db.execute("SELECT * FROM recipes WHERE id = ?", id,)
    name = recipes[0]["name"]
    ingredients = recipes[0]["ingredients"]
    instructions = recipes[0]["instructions"]
    category = recipes[0]["category"]
    preparation_time = recipes[0]["preparation_time"]
    cooking_time = recipes[0]["cooking_time"]

    if not recipes:
        flash("No recipes!", "warning")
        return redirect("/")
    next_recipe = db.execute("SELECT * FROM recipes WHERE id = ?", (id + 1,))
    prev_recipe = db.execute("SELECT * FROM recipes WHERE id = ?", (id - 1,))

    return render_template("recipe.html", id=id, name=name, ingredients=ingredients, instructions=instructions, category=category, preparation_time=preparation_time, cooking_time=cooking_time, next_recipe=next_recipe, prev_recipe=prev_recipe)



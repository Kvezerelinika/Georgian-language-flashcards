from flask import Flask
from flask_session import Session
from cs50 import SQL

def create_app():
    from .routes import main
    app = Flask(__name__, template_folder='../templates', static_folder="../static")

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['DATABASE'] = 'database.db'
    app.register_blueprint(main)


    Session(app)

    # Configure CS50 Library to use SQLite database
    app.db = SQL("sqlite:///database.db")

    return app

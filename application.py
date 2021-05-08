import os

from flask import Flask, session, redirect, render_template, request, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# DATABASE_URL = 'postgres://bzhtmusobeniig:9f855087930981b86cf77bf631e56d73b4bd982c69a50705a72c9f4d894368d9@ec2-54-87-112-29.compute-1.amazonaws.com:5432/diecrpvcd7dm3'
engine = create_engine(os.getenv("DATABASE_URL"))
database = scoped_session(sessionmaker(bind=engine))
db = database()

# Login required function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# INDEX
@app.route("/", methods=["GET","POST"])
@login_required
def index():
    return render_template("index.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    # Make sure no one's logged in
    session.clear()

    # POST METHOD
    if request.method == "POST":

        # Checks username
        if not request.form.get("email"):
            return render_template("error.html", message="Must Provide Username")
        # Checks password
        elif not request.form.get("password"):
            return render_template("error.html", message="Must Provide Password")

        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          {"email": request.form.get("email")}).fetchall()

        # Check username and password validity
        if len(rows) != 1:
            return render_template("error.html", message="Invalid Username")
        elif not check_password_hash(rows[0]["pass"], request.form.get("pass")):
            return render_template("error.html", message="Wrong Password")

        # Remember session id
        session['user_id'] = rows[0]["userid"]

        # Redirect to main page
        return redirect("/")

    # GET METHOD
    else:
        return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    # Make sure no one's logged in
    session.clear()

    # When user POST
    if request.method == "POST":

        rows = db.execute("SELECT * FROM users").fetchall()
        n = len(rows)

        # Check if username
        if not request.form.get("email"):
            return render_template("error.html", message="Must Provide Email")
        for i in range(n):
            if request.form.get("email") in rows[i]["email"]:
                return render_template("error.html", message="Email Taken")

        # Check Password and Confirmation
        if not request.form.get("pass"):
            return render_template("error.html", message="Must Provide Password")
        elif not request.form.get("confirm"):
            return render_template("error.html", message="Must Provide Password Confirmation")
        elif request.form.get("pass") != request.form.get("confirm"):
            return render_template("error.html", message="Password Confirmation Wrong")

        email = request.form.get("email")
        password = request.form.get("pass")

        hash_password = generate_password_hash(password)

        # Adds data to users table
        db.execute("INSERT INTO users (id,username, password) VALUES (:id,:username,:password)",
                   {"id": n + 1, "username": email, "password": hash_password})

        # Changes session user_id
        session['user_id'] = n + 1

        db.commit()

        # Redirect to main page
        return redirect("/")

    # When user GET
    else:
        return render_template("register.html")
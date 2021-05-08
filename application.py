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
# DATABASE_URL = 'postgresql://bzhtmusobeniig:9f855087930981b86cf77bf631e56d73b4bd982c69a50705a72c9f4d894368d9@ec2-54-87-112-29.compute-1.amazonaws.com:5432/diecrpvcd7dm3'
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
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    locations = []
    rows = db.execute("SELECT * FROM locations WHERE userid=:user", {"user": session['user_id']}).fetchall()
    for row in rows:
        month = row['time'][0:2]
        date = row['time'][3:5]
        locations.append([row['place'], row['city'], date, month])

    return render_template("index.html", locations=locations)


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    # Make sure no one's logged in
    session.clear()

    # POST METHOD
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # Checks Email
        if not email:
            return render_template("error.html", message="Must Provide Email")
        # Checks password
        if not password:
            return render_template("error.html", message="Must Provide Password")

        rows = db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).fetchall()

        # Check username and password validity
        if len(rows) != 1:
            return render_template("error.html", message="Invalid Email")
        elif not check_password_hash(rows[0]["pass"], password):
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

        email = request.form.get("email")
        password = request.form.get("password")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        hash_password = generate_password_hash(password)

        # Check Email
        if not email:
            return render_template("error.html", message="Must Provide Email")
        for i in range(n):
            if email in rows[i]["email"]:
                return render_template("error.html", message="Email Taken")

        # Check Password
        if not password:
            return render_template("error.html", message="Must Provide Password")
        # Check Firstname
        if not firstname:
            return render_template("error.html", message="Must Provide Firstname")
        # Check Lastname
        if not lastname:
            return render_template("error.html", message="Must Provide Lastname")

        # Adds data to users table
        db.execute("INSERT INTO users (userid, firstname, lastname, email, pass) \
                    VALUES (:id,:first,:last,:email,:password)",
                   {"id": n + 1, "first": firstname, "last": lastname, "email": email, "password": hash_password})

        # Changes session user_id
        session['user_id'] = n + 1

        db.commit()

        # Redirect to main page
        return redirect("/medicalinfo")

    # When user GET
    else:
        return render_template("register.html")

# Medical Info
@app.route("/medicalinfo", methods=["GET", "POST"])
@login_required
def medicalinfo():
    if request.method == "POST":
        userid = session['user_id']
        vaccine = request.form['vaccine']
        covid = request.form['covid']
        db.execute("UPDATE users SET vacc = :vaccine, covid = :covid WHERE userid = :userid",
                    {"vaccine": vaccine, "covid": covid, "userid": userid})
        db.commit()
        return redirect("/")
    else:
        return render_template("medinfo.html")
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
        if session.get('user_id') is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# # ADD
# @app.route("/")
# def add():

# INDEX
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        location = request.form.get('location')
        location_arr = location.split(',')
        place = location_arr[0]
        city = location_arr[2][1:] + "," + location_arr[3]
        date = request.form["date"]

        db.execute("INSERT INTO locations VALUES (:id, :place, :time, :city)",
                   {"id": session['user_id'], "place": place, "time": date, "city": city})
        db.commit()
        return redirect("/")
    else:
        locations = []
        rows = db.execute("SELECT * FROM locations WHERE userid=:user", {"user": session['user_id']}).fetchall()
        for row in rows:
            month_num = row['time'][5:7]
            if month_num == "01":
                month = "January"
            elif month_num == "02":
                month = "February"
            elif month_num == "03":
                month = "March"
            elif month_num == "04":
                month = "April"
            elif month_num == "05":
                month = "May"
            elif month_num == "06":
                month = "June"
            elif month_num == "07":
                month = "July"
            elif month_num == "08":
                month = "August"
            elif month_num == "09":
                month = "September"
            elif month_num == "10":
                month = "October"
            elif month_num == "11":
                month = "November"
            else:
                month = "December"
            date = row['time'][8:]
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

# Edit Profile
@app.route("/profile", methods=["GET", "POST"])
def profilepage():
    rows = db.execute("SELECT * FROM users WHERE userid=:userid", {"userid": session['user_id']}).fetchone()
    if request.method == "POST":
        if check_password_hash(rows['pass'], request.form.get('password')):
            db.execute("UPDATE users SET pass=:password, firstname=:firstname, lastname=:lastname, email=:email \
                        WHERE userid=:userid", {"password": generate_password_hash(request.form.get('newpassword')),
                                                "firstname": rows['firstname'], "lastname": rows['lastname'],
                                                "email": rows['email'], "userid": session['user_id']})
            db.commit()
        return redirect('/')
    return render_template('myprofile.html', email=rows['email'],
                           firstname=rows['firstname'], lastname=rows['lastname'])

# LOGOUT
@app.route("/logout")
def logout():

    # Clear Session
    session.clear()

    # Redirect to login form
    return redirect("/")

# COMPLETED
@app.route("/completed")
def completed():
    return render_template("completed.html")

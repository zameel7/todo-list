import os

from datetime import date
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///todolist.db")


@app.route("/")
def index():
    if not session:
        return render_template("index.html")
    else:
        return redirect("/main")

@app.route("/main", methods=["GET", "POST"])
@login_required
def main():
    if request.method == "GET":
        duetasks = db.execute("UPDATE tasks SET type = ? WHERE date('now') > date(dt)", "Overdue")
        tasks = db.execute("SELECT * FROM tasks WHERE user_id = ? AND type = ?" ,
                           session["user_id"], "Due");
        return render_template("main.html", tasks=tasks)
    else:
        id = request.form.get("id")
        print(id)
        db.execute("UPDATE tasks SET type=? WHERE user_id=? AND id = ?", "Done", session["user_id"], id)
        db.execute("UPDATE tasks SET cdt=? WHERE user_id=? AND id = ?", date.today(), session["user_id"], id)
        return redirect("/main")

@app.route("/addtask", methods=["GET", "POST"])
@login_required
def addT():
    if request.method == "GET":
        return render_template("add.html")
    else:
        deadline = request.form.get("deadline")
        topic = request.form.get("topic")
        priority = request.form.get("priority")

        if not deadline or not topic or not priority or isinstance(deadline, int):
            flash("Fill all the details!")
            return redirect("/addtask")

        y, m, d = [int(x) for x in deadline.split('-')]
        if date(y,m,d) < date.today():
            flash("Deadline already over!")
            return redirect("/addtask")

        if priority == "HIGH":
            priority = 3
        elif priority == "MEDIUM":
            priority = 2
        else:
            priority = 1
        db.execute("INSERT INTO tasks (user_id, priority, topic, type, dt) VALUES(?, ?, ?, ?, ?)", session["user_id"], priority, topic, "Due", deadline)
        return redirect("/main")

@app.route("/history")
@login_required
def history():
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", session["user_id"])
    return render_template("history.html", tasks=tasks)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/main")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Store name in name and password in db and check if previously exist
        name = request.form.get("username")
        prev = db.execute("SELECT EXISTS(SELECT * FROM users WHERE username = ?) ", name)
        prev = [i for i in prev[0].items()]
        if prev[0][1] or not name:
            return apology("Username invalid or not available")

        # Check if passwords match
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        if not password or password != confirm:
            return apology("Password invalid")

        # Store the details in the database
        else:
            hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, hash)
            flash("User had been registered successfully!")
            return redirect("/login")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
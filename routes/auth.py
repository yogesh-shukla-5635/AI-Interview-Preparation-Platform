from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from utils.database import create_user, get_user_by_email

auth = Blueprint("auth", __name__)


# -----------------------
# Home (Login Page)
# -----------------------
@auth.route("/")
def home():
    return render_template("login.html")


# -----------------------
# Signup
# -----------------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)

        if user:
            return "Email already registered."

        hashed_password = generate_password_hash(password)

        create_user(name, email, hashed_password)

        return redirect(url_for("auth.home"))

    return render_template("signup.html")


# -----------------------
# Login
# -----------------------
@auth.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    user = get_user_by_email(email)

    if user and check_password_hash(user["password"], password):
         session["user_id"] = user["id"]
         session["user_name"] = user["name"]
         session["role"] = user["role"]

    # Admin Login
         if user["role"] == "admin":
             return redirect(url_for("admin.admin_dashboard"))

    # Normal User
         return redirect(url_for("profile.dashboard"))

    return "Invalid Email or Password"

# -----------------------
# Logout
# -----------------------
@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.home"))
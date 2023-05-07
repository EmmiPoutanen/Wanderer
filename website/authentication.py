from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from website.static.db import db


authentication = Blueprint("authentication", __name__)


@authentication.route("/login")
def login():
    return render_template("login.html")


@authentication.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    # Check if the user actually exists
    # Has the password and compare it to the password in database
    if not user or not check_password_hash(user.password, password):
        # If the user doesn"t exist or password is wrong, relaod page with error
        return redirect(url_for("authentication.login"))

    # Login passed, redirect to home screen
    login_user(user, remember=remember)
    return redirect(url_for("main.home"))


@authentication.route("/signup")
def signup():
    return render_template("signup.html")


@authentication.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if email exists in database
    user = User.query.filter_by(email=email).first()

    if user:
        # If a user is found, redirect back to signup page with error text
        return redirect(url_for("authentication.signup"))

    # Create a new user with the form data. Hash the password with sha256
    new_user = User(email=email, password=generate_password_hash(password,
                                                                 method="sha256"))

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    # Redirect to login screen
    return redirect(url_for("authentication.login"))


@authentication.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("authentication.login"))
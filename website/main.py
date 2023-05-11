from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from .models import Event
from website.static.db import db


main = Blueprint("main", __name__)


@main.route("/home")
@login_required
def home():
    events = Event.query.all()
    return render_template("home.html", events=events)


@main.route("/create_event")
@login_required
def create_event():
    events = Event.query.all()
    return render_template("create_event.html", events=events)


@main.route("/create_event", methods=["POST"])
@login_required
def create_event_post():
    # Get data from html form
    name = request.form.get("name")
    description = request.form.get("description")
    category = request.form.get("category")
    date = datetime.strptime(request.form.get("date"), "%Y-%m-%dT%H:%M%S")
    max_participants = request.form.get("max_participants")
    location = request.form.get("location")

    if name == "" or description == "" or category == 0 or max_participants == "" or int(max_participants) <= 0:
        flash("Pakollinen kenttä puuttuu")
        return redirect(url_for("main.create_event"))

    new_event = Event(user_id=current_user.id,
                      name=name,
                      description=description,
                      category=category,
                      date=date,
                      max_participants=max_participants,
                      location=location)
    # Adding the event to the database
    db.session.add(new_event)
    db.session.commit()

    events = Event.query.all()
    return redirect(url_for("main.home" , events=events))


@main.route("/profile")
@login_required
def profile():
    events = Event.query.all()
    return render_template("profile.html", events=events)


@main.route("/event/")
@main.route("/event/<eventid>")
@login_required
def event(eventid=1):
    events = Event.query.all()
    # Pass the clicked event to event screen
    event = Event.query.filter_by(id=eventid).first()
    return render_template("event.html", events=events, event=event)

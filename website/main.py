from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from .models import Event
from website.static.db import db


main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    events = Event.query.all()
    return render_template("home.html", events=events)


@main.route('/create_event')
@login_required
def create_event():
    events = Event.query.all()
    return render_template("create_event.html", events=events)


@main.route('/create_event', methods=["POST"])
@login_required
def create_event_post():
    name = request.form.get('name')
    description = request.form.get('description')
    category = request.form.get('category')
    date = datetime.now()
    max_participants = request.form.get('max_participants')
    location = request.form.get('location')

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

    return redirect(url_for("main.home"))


@main.route('/profile')
@login_required
def profile():
    events = Event.query.all()
    return render_template("profile.html", events=events)

@main.route('/event/')
@main.route('/event/<eventid>')
@login_required
def event(eventid=1):
    print("Hello")
    events = Event.query.all()
    event = Event.query.filter_by(id=eventid).first()
    return render_template("event.html", events=events, event=event)

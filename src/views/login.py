from flask import Blueprint, Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.orm import Mapped, relationship
from ..models import Profile,db

bp = Blueprint("login", __name__, url_prefix="/login")

@bp.route('/', methods=["GET"])
def login():
    profiles = db.session.execute(select(Profile)).scalars().all()
    return render_template('login.html.jinja',profiles=profiles)

@bp.route('/', methods=["POST"])
def check_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if():
        return "LOGIN Success",200
    else:
        return "Login Failed",401

@bp.route('/create' ,methods=["POST"])
def create_db():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    print(username)
    print(password)
    profile = Profile()
    profile.Username=username
    profile.Password=password
    db.session.add(profile)
    db.session.commit()

    return 'Success',200



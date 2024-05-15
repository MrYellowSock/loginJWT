from flask import Blueprint, Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.orm import Mapped, relationship
from ..models import Profile,db

bp = Blueprint("register", __name__, url_prefix="/register")

@bp.route("/" ,methods=["GET"])
def register():
    profiles = db.session.execute(select(Profile)).scalars().all()
    return render_template("register.html.jinja",profiles=profiles)

@bp.route("/" ,methods=["POST"])
def create_account():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not username or not password:
        return "fail",400
    print(username)
    print(password)
    profile = Profile()
    profile.Username=username
    profile.Password=password
    db.session.add(Profile)
    db.session.commit()
    return render_template("register.html.jinja")
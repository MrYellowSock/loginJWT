from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from . import db


class Profile(db.Model):
    id = db.Column(db.Integer,index=True, primary_key=True)
    Username = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(20), unique=False, nullable=False)
    token = db.Column(db.String(50))
    
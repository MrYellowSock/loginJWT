from flask import Blueprint, Flask, redirect,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
from typing import List
import jwt
from sqlalchemy import Column, ForeignKey, Integer, String, select, update
from sqlalchemy.orm import Mapped, relationship
from ..models import Profile,db
import random
import redis
import smtplib
from email.message import  EmailMessage


bp = Blueprint("login", __name__, url_prefix="/login")
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
server = smtplib.SMTP('smtp.gmail.com')
server.starttls()

from_mail = 'yuwansiri_t2@silpakorn.edu'
server.login(from_mail,'jwpu vmtg qmch fqdo')
to_mail = 'thanatornsense2468@gmail.com'

msg = EmailMessage()
msg['Subject'] = "OTP Verification"
msg['From'] = from_mail
msg['To'] = to_mail

expiration_time = 60

def otpRandom():
    otp = ""
    for i in range(6):
        otp+=str(random.randint(0,9))
    return otp

@bp.route('/', methods=["POST"])
def check_login():
    username = request.form.get("Username", "")
    password = request.form.get("Password", "")
    print(username)
    print(password)
    checkUser = Profile.query.filter(Profile.Username==username).all()
    checkPass = Profile.query.filter(Profile.Password==password).all()
    if(checkUser and checkPass):        
        random = otpRandom()
        r.set(username,random)
        msg.set_content("Your OTP is : "+r.get(username))
        server.send_message(msg)
        print('OTP : ',random)
        r.expire(username,60)
        return {'status':'OTP send'},200
    else:
        return {'status':'Login Failed'},401

@bp.route('/otp', methods=["POST"])
def check_otp():
    username = request.form.get("Username", "")
    otp = request.form.get("otp", "")
    print("Enter username : " ,username)
    print("Enter OTP : " ,otp)
    if otp == r.get(username):
        return {'status':'OTP success'},200
    else:
        return {'status':'OTP Failed'},401
    
@bp.route('/token',methods=['POST'])
def check_token():
    username = request.form.get("Username", "")
    encoded_jwt = jwt.encode({username: r.get(username)}, "secret", algorithm="HS256")
    r.delete(username)
    values={}
    values.update({
        "token":encoded_jwt
    })
    db.session.execute(update(Profile).where(Profile.Username == username).values(values))
    db.session.commit()
    print(encoded_jwt)
    return {'status':'Token Success'},200

@bp.route('/create' ,methods=["POST"])
def create_db():
    username = request.form.get("Username", "")
    password = request.form.get("Password", "")
    print(username)
    print(password)
    profile = Profile()
    profile.Username=username
    profile.Password=password
    db.session.add(profile)
    db.session.commit()
    
    return {"status":'Create Success'},200



from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import jwt
import hashlib
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime, timedelta

app = Flask(__name__)

client = MongoClient('mongodb+srv://arysanjaya:testing1234@cluster0.7irhzom.mongodb.net/?retryWrites=true&w=majority')
db = client.dbimaproject

SECRET_KEY = 'imaproject'

@app.route('/')
def home():
   token_receive = request.cookies.get("mytoken")
   try:
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    user_info = db.user.find_one({"username": payload["id"]})
    return render_template('lp.html', user_info=user_info)
   except (jwt.ExpiredSignatureError,jwt.exceptions.DecodeError):
    return render_template('lp.html')

@app.route('/login')
def login():
    msg = request.args.get('msg')
    return render_template('login.html', msg=msg)


# sign in client
@app.route("/sign_in", methods=["POST"])
def sign_in():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.user.find_one({"username": username_receive,"password": pw_hash,})
    if result:
        payload = {"id": username_receive,"exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"result": "success","token": token,})
    else:
        return jsonify({"result": "fail","msg": "We could not find a user with that id/password combination",})
    
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form["username_give"]
    name_receive = request.form["name_give"]
    password_receive = request.form["password_give"]
    password_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    date_receive = request.form.get("date_give")
    doc = {
        "username": username_receive,
        "name": name_receive,
        "password": password_hash,
        "date": date_receive,
    }
    db.user.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    user = db.user.find_one({"username": username_receive})
    print(user)
    exists = bool(user)
    return jsonify({'result': 'success', 'exists': exists})

# sign in admin
@app.route("/sign_in_admin", methods=["POST"])
def sign_in_admin():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.admin.find_one({"username": username_receive,"password": pw_hash,})
    if result:
        payload = {"id": username_receive,"exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"result": "success","token": token,})
    else:
        return jsonify({"result": "fail","msg": "We could not find a user with that id/password combination",})
    
@app.route('/sign_up_admin/save', methods=['POST'])
def sign_up_admin():
    username_receive = request.form["username_give"]
    name_receive = request.form["name_give"]
    password_receive = request.form["password_give"]
    password_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    date_receive = request.form.get("date_give")
    doc = {
        "username": username_receive,
        "name": name_receive,
        "password": password_hash,
    }
    db.admin.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up_admin/check_dup_admin', methods=['POST'])
def check_dup_admin():
    username_receive = request.form['username_give']
    user = db.admin.find_one({"username": username_receive})
    print(user)
    exists = bool(user)
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/activity')
def activity():
   token_receive = request.cookies.get("mytoken")
   try:
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    user_info = db.user.find_one({"username": payload["id"]})
    return render_template('activity.html', user_info=user_info)    
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="You Need To Login First"))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="You Need To Login First"))

@app.route('/health_education')
def health_education():
   token_receive = request.cookies.get("mytoken")
   try:
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    user_info = db.user.find_one({"username": payload["id"]})
    return render_template('Healthed.html', user_info=user_info)    
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="You Need To Login First"))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="You Need To Login First"))
   

@app.route('/workout_training')
def workout_training():
   token_receive = request.cookies.get("mytoken")
   try:
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    user_info = db.user.find_one({"username": payload["id"]})
    return render_template('', user_info=user_info)    
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="You Need To Login First"))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="You Need To Login First"))
   
@app.route('/suggestion', methods=['POST'])
def suggestion():
   name_receive = request.form['name_give']
   subject_receive = request.form['subject_give']
   message_receive = request.form['message_give']
   doc = {
      'name': name_receive,
      'subject': subject_receive,
      'message': message_receive,
   }
   db.suggestion.insert_one(doc)
   return jsonify({'result':'success',"msg": "Saran anda sudah terkirim, Terimakasih!"})

@app.route('/dashboard')
def dashboard():
   return render_template('loginadmin.html')

@app.route('/dashboard2')
def dashboard2():
   return render_template('dashboard2.html')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
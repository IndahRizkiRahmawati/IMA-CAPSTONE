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



# login
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



# activity
@app.route('/activity')
def activity():
   token_receive = request.cookies.get("mytoken")
   try:
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    user_info = db.user.find_one({"username": payload["id"]})
    activity_user = db.activity.find({"username": user_info['username']},{'_id':False})
    activity_list = list(activity_user)
    return render_template('activity.html', user_info=user_info, activity_user=activity_list)    
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="You Need To Login First"))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="You Need To Login First"))
   
@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    username_receive = request.form['user_give']
    count = db.activity.count_documents({})
    date_receive = request.form.get("date_give")
    num = count + 1
    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done':0,
        'username':username_receive,
        'date': date_receive
    }
    db.activity.insert_one(doc)
    return jsonify({'msg':'Data Disimpan!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.activity.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update Selesai!'})

@app.route("/bucket/delete", methods=["POST"])
def delete_bucket():
    num_receive = request.form["num_give"]
    db.activity.delete_one(
        {'num': int(num_receive)}
    )
    return jsonify({'msg': 'Delete Selesai!'})



# health education
@app.route('/health_education')
def health_education():
   token_receive = request.cookies.get("mytoken")
   try:
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    user_info = db.user.find_one({"username": payload["id"]})
    healthedu = db.healthedu.find({},{'_id':False})
    return render_template('Healthed.html', user_info=user_info, healthedu=healthedu)    
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="You Need To Login First"))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="You Need To Login First"))
   



# workout training
@app.route('/workout_training')
def workout_training():
   token_receive = request.cookies.get("mytoken")
   try:
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    user_info = db.user.find_one({"username": payload["id"]})
    workouttrain = db.workouttrain.find({},{'_id':False})
    workouttrain2 = db.workouttrain.find({},{'_id':False})
    return render_template('workout.html', user_info=user_info, workouttrain=workouttrain, workouttrain2=workouttrain2)    
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="You Need To Login First"))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="You Need To Login First"))



# suggestion box landing page
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

# ------------------------------------------------------------DASHBOARD--------------------------------------------------------------------------------

# login dashboard
@app.route('/dashboard')
def dashboard():
   return render_template('loginadmin.html')




# dashboard
@app.route('/dashboard2')
def dashboard2():
   return render_template('admindash.html')

@app.route('/dashgetdata', methods=['GET'])
def dashgetdata():
   user = list(db.user.find({},{'_id':False}))
   return jsonify({'user':user})

@app.route('/dashgetdata2', methods=['GET'])
def dashgetdata2():
   suggestion = list(db.suggestion.find({},{'_id':False}))
   return jsonify({'suggestion':suggestion})

@app.route("/dashboard/delete", methods=["POST"])
def delete_user():
    name_receive = request.form["name_give"]
    db.user.delete_one(
        {'name': name_receive}
    )
    return jsonify({'msg': 'Delete Selesai!'})

@app.route("/dashboard/delete2", methods=["POST"])
def delete_suggestion():
    name_receive = request.form["name_give"]
    db.suggestion.delete_one(
        {'name': name_receive}
    )
    return jsonify({'msg': 'Delete Selesai!'})




# activity dashboars
@app.route('/atdash')
def atdash():
   return render_template('ATdash.html')

@app.route('/atgetdata', methods=['GET'])
def atgetdata():
   activity = list(db.activity.find({},{'_id':False}))
   return jsonify({'activity':activity})

@app.route("/atdash/delete", methods=["POST"])
def delete_at():
    name_receive = request.form["name_give"]
    db.activity.delete_one(
        {'username': name_receive}
    )
    return jsonify({'msg': 'Delete Selesai!'})




# heatlh education dashboars
@app.route('/hedash')
def hedash():
   return render_template('HEdash.html')

@app.route('/hegetdata', methods=['GET'])
def hegetdata():
   healtheducation = list(db.healthedu.find({},{'_id':False}))
   return jsonify({'healtheducation':healtheducation})

@app.route('/hedash/add')
def hedash_add():
   return render_template('addhealthedu.html')

@app.route("/tambah_he/save", methods=["POST"])
def tambahHE():
    num = db.healthedu.count_documents({})
    judul_recieve = request.form['judul_give']
    catatan_recieve = request.form['catatan_give']
    id = num + 1
    if "gambar_give" in request.files:
        file = request.files["gambar_give"]
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        file_path = f"content_he/{judul_recieve}.{extension}"
        file.save("./static/" + file_path)
    doc = {
        "judul":judul_recieve,
        "catatan":catatan_recieve,
        "gambar":file_path,
        "id":id
    }
    db.healthedu.insert_one(doc)
    return jsonify({'result': 'success','msg':'Health Education Added'})

@app.route('/hedash/edit/<id>')  
def hedash_edit(id):
   find = db.healthedu.find_one({'id':int(id)},{'_id':False})
   return render_template('edithealthedu.html',data=find)


@app.route('/edit_he/save', methods =["POST"])
def editHE():
   id_receive = request.form['id_give']
   judul_recieve = request.form['judul_give']
   catatan_recieve = request.form['catatan_give']
   if "gambar_give" in request.files:
    file = request.files["gambar_give"]
    filename = secure_filename(file.filename)
    extension = filename.split(".")[-1]
    file_path = f"content_he/{judul_recieve}.{extension}"
    file.save("./static/" + file_path)
    doc = {
        "judul":judul_recieve,
        "catatan":catatan_recieve,
        "gambar":file_path
    }
    db.healthedu.update_one({'id':int(id_receive)},{'$set':doc})
    return jsonify({'result': 'success','msg':'Health Education Edited'})
   
@app.route('/health_education/delete', methods=["POST"])
def delete_he():
   judul_receive = request.form["judul_give"]
   db.healthedu.delete_one(
      {'judul': judul_receive}
   )
   return jsonify({'msg': 'Delete Selesai!'})




# workout dashboars
@app.route('/wtdash')
def wtdash():
   return render_template('WTdash.html')

@app.route('/wtgetdata', methods=['GET'])
def wtgetdata():
   workouttraining = list(db.workouttrain.find({},{'_id':False}))
   return jsonify({'workouttraining':workouttraining})

@app.route('/wtdash/add')
def wtdash_add():
   return render_template('addworkout.html')

@app.route("/tambah_wt/save", methods=["POST"])
def tambahWT():
    num = db.workouttrain.count_documents({})
    judul_recieve = request.form['judul_give']
    catatan_recieve = request.form['catatan_give']
    link_recieve = request.form['link_give']
    id = num + 1
    if "cover_give" in request.files:
        file = request.files["cover_give"]
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        file_path = f"content_wt/{judul_recieve}.{extension}"
        file.save("./static/" + file_path)
    doc = {
        "judul":judul_recieve,
        "catatan":catatan_recieve,
        "cover":file_path,
        "link":link_recieve,
        "id":id
    }
    db.workouttrain.insert_one(doc)
    return jsonify({'result': 'success','msg':'Workout Training Added'})

@app.route('/wtdash/edit/<id>')
def wtdash_edit(id):
   find = db.workouttrain.find_one({'id':int(id)},{'_id':False})
   return render_template('editworkout.html',data=find)

@app.route('/edit_wt/save', methods =["POST"])
def editWT():
    id_receive = request.form['id_give']
    judul_recieve = request.form['judul_give']
    catatan_recieve = request.form['catatan_give']
    link_recieve = request.form['link_give']
    if "cover_give" in request.files:
        file = request.files["cover_give"]
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        file_path = f"content_wt/{judul_recieve}.{extension}"
        file.save("./static/" + file_path)
    doc = {
        "judul":judul_recieve,
        "catatan":catatan_recieve,
        "cover":file_path,
        "link":link_recieve,
    }
    db.workouttrain.update_one({'id':int(id_receive)},{'$set':doc})
    return jsonify({'result': 'success','msg':'Workout Training Edited'})

@app.route('/workout_training/delete', methods=["POST"])
def delete_wt():
   judul_receive = request.form["judul_give"]
   db.workouttrain.delete_one(
      {'judul': judul_receive}
   )
   return jsonify({'msg': 'Delete Selesai!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
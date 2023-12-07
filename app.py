from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://indahrizki:indah004@cluster0.8yo7q7m.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('activity.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1 
    doc = {
        'num' : num, 
        'bucket' : bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        { 'num': int(num_receive) },
        { '$set': {'done': 1 }}
    )
    print(num_receive)
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form['num_give']
    result = db.bucket.delete_one({'num': int(num_receive)})

    if result.deleted_count > 0: 
        return jsonify({'msg': 'Delete successful!'})
    else:
        return jsonify({'msg': 'Bucket not found or already deleted!'})
     

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
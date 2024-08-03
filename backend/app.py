# backend/app.py
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_ref.document(data['uid']).set(data)
    return jsonify({"success": True}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_doc = user_ref.document(data['uid']).get()
    if user_doc.exists:
        return jsonify(user_doc.to_dict()), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/user/<uid>', methods=['GET', 'PUT'])
def user(uid):
    if request.method == 'GET':
        user_doc = user_ref.document(uid).get()
        if user_doc.exists:
            return jsonify(user_doc.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    elif request.method == 'PUT':
        data = request.get_json()
        user_ref.document(uid).update(data)
        return jsonify({"success": True}), 200

@app.route('/admin/users', methods=['GET'])
def get_all_users():
    users = [doc.to_dict() for doc in user_ref.stream()]
    return jsonify(users), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

import bcrypt
from flask import Blueprint, request, jsonify
from db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data['email']
    input_password = data['password'].encode('utf-8')

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    if user and bcrypt.checkpw(input_password, user['password'].encode('utf-8')):
        return jsonify({
            "status": "success",
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }), 200
    else:
        return jsonify({"status": "failed", "error": "Invalid credentials"}), 401

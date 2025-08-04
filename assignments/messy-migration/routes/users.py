import bcrypt
from flask import Blueprint, request, jsonify
from db import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    user_list = []
    for user in users:
        user_dict = dict(user)
        user_dict.pop("password", None)  # Remove password
        user_list.append(user_dict)
    return jsonify(user_list), 200



@users_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user:
        user_dict = dict(user)
        user_dict.pop("password", None)  # Remove password
        return jsonify(user_dict), 200
    return jsonify({"error": "User not found"}), 404


@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "Missing fields"}), 400

    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                 (data['name'], data['email'], hashed_pw.decode('utf-8')))
    conn.commit()
    return jsonify({"message": "User created"}), 201

@users_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", 
                 (data['name'], data['email'], user_id))
    conn.commit()
    return jsonify({"message": "User updated"}), 200

@users_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return jsonify({"message": f"User {user_id} deleted"}), 200

@users_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Missing 'name' query param"}), 400

    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()
    return jsonify([dict(user) for user in users]), 200

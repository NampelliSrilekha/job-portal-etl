import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from services.user_services import UserServices
from models.users import User
from utils.json_response import success_response, error_response, object_to_json, list_to_json

app = Flask(__name__)
user_services = UserServices()

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    try:
        user = User(
            user_id=data['user_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            personal_email=data['personal_email'],
            phone=data['phone'],
            Password_hash=data['Password_hash'],
            profile_picture=data.get('profile_picture')
        )
        user_services.bulk_insert_users([user])
        return jsonify(success_response("User created successfully", object_to_json(user), 201))
    except KeyError as e:
        return jsonify(error_response(f"Missing field: {str(e)}", 400))

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    data = request.get_json()

    if not user_services.user_exists(user_id):
        return jsonify(error_response("User not found", 404))

    try:
        user = User(
            user_id=user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            personal_email=data['personal_email'],
            phone=data['phone'],
            Password_hash=data['Password_hash'],
            profile_picture=data.get('profile_picture')
        )
        user_services.update_user(user)
        return jsonify(success_response("User updated successfully", object_to_json(user), 200))
    except KeyError as e:
        return jsonify(error_response(f"Missing field: {str(e)}", 400))

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete an existing user"""
    if not user_services.user_exists(user_id):
        return jsonify(error_response("User not found", 404))
    
    user_services.delete_user(user_id)
    return jsonify(success_response("User deleted successfully", None, 200))

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get details of a single user"""
    user = user_services.get_user_by_id(user_id)
    
    if user:
        return jsonify(success_response("User retrieved successfully", object_to_json(user), 200))
    else:
        return jsonify(error_response("User not found", 404))

@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    users = user_services.get_all_users()
    return jsonify(success_response("Users retrieved successfully", list_to_json(users), 200))

if __name__ == '__main__':
    app.run(debug=True)
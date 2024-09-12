#!/usr/bin/env python3
"""Set up a basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index():
    """The index page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Create a new user"""
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Log the user in"""
    email = request.form['email']
    password = request.form['password']
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie('session_id', session_id)
    return resp


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Log the user out"""
    session_id = request.cookies.get('session_id')
    u = AUTH.get_user_from_session_id(session_id)
    if u is None:
        abort(403)
    AUTH.destroy_session(u.id)
    return redirect('/')


@app.route('/profile')
def profile():
    """Log the user out"""
    session_id = request.cookies.get('session_id')
    u = AUTH.get_user_from_session_id(session_id)
    if u is None:
        abort(403)
    return jsonify({"email": u.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Get the token that will be used to reset the password"""
    email = request.form['email']
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_pwd():
    """Rest the user's password"""
    email = request.form['email']
    reset_token = request.form['reset_token']
    new_password = request.form['new_password']
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """Register the user in the database"""
    data = {'email': email, 'password': password}
    payload = {"email": email, "message": "user created"}
    r = requests.post('http://localhost:5000/users', data=data)
    assert r.status_code == 200
    assert r.json() == payload


def log_in_wrong_password(email: str, password: str) -> None:
    data = {'email': email, 'password': password}
    payload = {"email": email, "message": "user created"}
    r = requests.post('http://localhost:5000/sessions', data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    data = {'email': email, 'password': password}
    payload = {"email": email, "message": "logged in"}
    r = requests.post('http://localhost:5000/sessions', data=data)
    assert r.status_code == 200
    assert r.json() == payload
    return r.cookies['session_id']


def profile_unlogged() -> None:
    cookies = {'session_id': '75c89af8-1729-44d9-a592-41b5e59de9a1'}
    r = requests.get('http://localhost:5000/profile', cookies=cookies)
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    cookies = {'session_id': session_id}
    r = requests.get('http://localhost:5000/profile', cookies=cookies)
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    cookies = {'session_id': session_id}
    payload = {"message": "Bienvenue"}
    r = requests.delete('http://localhost:5000/sessions', cookies=cookies)
    assert r.status_code == 200
    assert r.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    data = {'email': email}
    r = requests.post('http://localhost:5000/reset_password', data=data)
    assert r.status_code == 200
    return r.json().get('reset_token', None)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    payload = {"email": email, "message": "Password updated"}
    r = requests.put('http://localhost:5000/reset_password', data=data)
    assert r.status_code == 200
    assert r.json() == payload


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

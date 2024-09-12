#!/usr/bin/env python3
"""Create a hash of the current password"""
import bcrypt
from db import DB
from typing import Union
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user in the database"""
        try:
            u = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pwd = _hash_password(password)
            u = self._db.add_user(email, pwd)
            return u

    def valid_login(self, email: str, password: str) -> bool:
        """Check if a user with there credentials exists"""
        try:
            u = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), u.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a session for this user"""
        try:
            u = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(u.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Find a user by his session id"""
        if session_id is None:
            return None
        try:
            u = self._db.find_user_by(session_id=session_id)
            return u
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Delete the current user's session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> Union[str, None]:
        """Create a reset_token attribute for this user"""
        try:
            u = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(u.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the user's password"""
        try:
            u = self._db.find_user_by(reset_token=reset_token)
            pwd = _hash_password(password)
            new_data = {'hashed_password': pwd, 'reset_token': None}
            self._db.update_user(u.id, **new_data)
        except NoResultFound:
            raise ValueError


def _generate_uuid() -> str:
    """Generate a string representation of a new UUID"""
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

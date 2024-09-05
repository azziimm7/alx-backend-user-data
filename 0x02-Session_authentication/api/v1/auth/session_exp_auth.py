#!/usr/bin/env python3
"""The Session Auth class"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
from os import getenv
import uuid


class SessionExpAuth(SessionAuth):
    """A class that performs session authentication"""
    def __init__(self):
        """Initialize a session that can expire"""
        super().__init__()
        duration = getenv('SESSION_DURATION', '0')
        self.session_duration = 0
        if duration.isdigit():
            self.session_duration = int(duration)

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID"""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary['user_id']
        if 'created_at' not in session_dictionary:
            return None
        created_at = session_dictionary['created_at']
        span = timedelta(seconds=self.session_duration)
        if created_at + span < datetime.now():
            return None
        return session_dictionary['user_id']

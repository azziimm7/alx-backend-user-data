#!/usr/bin/env python3
"""The Session Auth class"""
from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession
from os import getenv
import uuid


class SessionDBAuth(SessionExpAuth):
    """A class that save the session in the database"""

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id and save it in the database"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**session_dictionary)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID from the database based on a Session ID"""
        if session_id is None:
            return None
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        created_at = sessions[0].created_at
        span = timedelta(seconds=self.session_duration)
        if created_at + span < datetime.now():
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """Delete the user session from the database"""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        sessions[0].remove()
        return True

#!/usr/bin/env python3
"""The Auth class"""
import re
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """A class that performs authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if the path requires authentication

        Returns:
            True: if
                    - path is None
                    - excluded_paths is None or empty
            False: if
                    - path is in excluded_paths
        """
        path_with_slash = None
        if not (path and excluded_paths):
            return True
        if path[-1] != '/':
            path_with_slash = path + '/'
        if path in excluded_paths or path_with_slash in excluded_paths:
            return False
        for p in excluded_paths:
            if path.startswith(p):
                return False
            if p[-1] == '*' and path.startswith(p[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the value  of authorization header"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """A template that will be used to return the current user"""
        return None

    def session_cookie(self, request=None):
        """Return a cookie value from a request"""
        if request is None:
            return None
        _my_session_id = getenv('SESSION_NAME', None)
        return request.cookies.get(_my_session_id)

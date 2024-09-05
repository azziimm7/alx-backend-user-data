#!/usr/bin/env python3
"""The Basic Auth class"""
import base64
from .auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """A class that performs basic authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return the Base64 part of the Authorization header"""
        if (authorization_header is None
                or type(authorization_header) is not str):
            return None
        fields = authorization_header.split()
        if fields[0] != 'Basic':
            return None
        return fields[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Return the decoded value of a Base64 string"""
        if (base64_authorization_header is None
                or type(base64_authorization_header) is not str):
            return None
        try:
            return base64.b64decode(base64_authorization_header,
                                    validate=True).decode('utf-8')
        except Exception:
            None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract the username and password"""
        if (decoded_base64_authorization_header is None
                or type(decoded_base64_authorization_header) is not str
                or ':' not in decoded_base64_authorization_header):
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Extract a user object from the database"""
        if (user_email is None or type(user_email) is not str
                or user_pwd is None or type(user_pwd) is not str):
            return None
        try:
            users = User.search({'email': user_email})
        except KeyError:
            return None
        for u in users:
            if u.is_valid_password(user_pwd):
                return u

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user based on the request header"""
        header = self.authorization_header(request)
        base_64_creds = self.extract_base64_authorization_header(header)
        decoded_creds = self.decode_base64_authorization_header(base_64_creds)
        creds = self.extract_user_credentials(decoded_creds)
        return self.user_object_from_credentials(*creds)

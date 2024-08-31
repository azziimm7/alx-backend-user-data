#!/usr/bin/env python3
"""
A module that is used for encryption purposes
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypt a password"""
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if two passwords match"""
    return (bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password))

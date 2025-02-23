# utils/common_utils.py
import hashlib

def hash_password(password):
    """Hash password securely"""
    return hashlib.sha256(password.encode()).hexdigest()

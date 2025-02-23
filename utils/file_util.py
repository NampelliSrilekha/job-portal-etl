# utils/file_utils.py
import os

def file_exists(file_path):
    """Check if a file exists"""
    return os.path.exists(file_path)

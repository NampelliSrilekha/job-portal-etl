# utils/json_util.py
import json
from models.users import User
from models.membership import Membership

def read_json(file_path, model):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Convert dictionaries to model objects (User or Membership)
            if model == User:
                # If the model is User, return a list of User objects
                return [User(**user) for user in data]
            elif model == Membership:
                # If the model is Membership, return a list of Membership objects
                return [Membership(**membership) for membership in data]
            else:
                raise ValueError("Unsupported model type")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")
        return []
    except ValueError as e:
        print(e)
        return []

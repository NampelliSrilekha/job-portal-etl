# main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.user_services import UserServices
from services.membership_services import MembershipServices  # Import MembershipServices
from utils.json_util import read_json
from models.users import User  # Import User model
from models.membership import Membership  # Import Membership model

def main():
    # Initialize services
    user_service = UserServices()
    membership_service = MembershipServices()  # Initialize MembershipServices

    # Load users from JSON file
    user_input_file = 'json_data/user.json'
    users = read_json(user_input_file, User)  # Pass User model

    if users:
        user_service.bulk_insert_users(users)

    # Load memberships from JSON file
    membership_input_file = 'json_data/membership.json'
    memberships = read_json(membership_input_file, Membership)  # Pass Membership model

    if memberships:
        membership_service.bulk_insert_memberships(memberships)  # Insert memberships

    # Close connections
    user_service.close_connection()
    membership_service.close_connection()  # Close membership service connection

if __name__ == "__main__":
    main()

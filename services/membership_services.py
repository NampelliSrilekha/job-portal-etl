# # services/membership_services.py
# import json
# from db.db_connection import DatabaseConnection
# from models.membership import Membership  # Ensure that your Membership model is correctly imported

# class MembershipServices:
#     def __init__(self):
#         self.db_connection = DatabaseConnection().connect()
#         self.cursor = self.db_connection.cursor()

#     def bulk_insert_memberships(self, memberships):
#         for membership_data in memberships:
#             membership = Membership(
#                 membership_id = membership_data["membership_id"],
#                 user_id = membership_data["user_id"],
#                 type_of_membership = membership_data["Type_of_membership"],
#                 active_date = membership_data["active_date"],
#                 expiry_date = membership_data["expiry_date"]
#             )
#             self.insert_membership(membership)

#     def insert_membership(self, membership):
#         query = """
#         INSERT INTO membership (membership_id, user_id, Type_of_membership, active_date, expiry_date, created_date, modified_date)
#         VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
#         """
#         self.cursor.execute(query, membership.to_tuple())
#         self.db_connection.commit()

#     def close_connection(self):
#         """Close database connection"""
#         if self.db_connection:
#             self.db_connection.close()

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db_connection import DatabaseConnection
from models.membership import Membership  # Import the User class

class MembershipServices:
    def __init__(self):
        self.db_connection = DatabaseConnection().connect()
        self.cursor = self.db_connection.cursor()

    def membership_exists(self, membership_id):
        """Check if a memberships exists in the database"""
        self.cursor.execute("SELECT COUNT(*) FROM membership WHERE membership_id = %s", (membership_id,))
        return self.cursor.fetchone()[0] > 0

    def bulk_insert_memberships(self, memberships):
        """Insert new users, skipping existing ones"""
        insert_query = """
        INSERT INTO membership (membership_id, user_id, Type_of_membership, active_date, expiry_date, created_date, modified_date)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """
        # Insert only new users (those that don't already exist)
        new_memberships = [membership.to_tuple() for membership in memberships if not self.membership_exists(membership.membership_id)]

        if new_memberships:
            try:
                self.cursor.executemany(insert_query, new_memberships)
                self.db_connection.commit()
                print(f"Inserted {self.cursor.rowcount} new memberships")
            except Exception as e:
                print(f"Error inserting memberships: {e}")
        else:
            print("No new memberships to insert.")

    def close_connection(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()
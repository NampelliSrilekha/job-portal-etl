# # services/user_services.py
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from db.db_connection import DatabaseConnection

# class UserServices:
#     def __init__(self):
#         self.db_connection = DatabaseConnection().connect()
#         self.cursor = self.db_connection.cursor()

#     def user_exists(self, user_id):
#         """Check if a user exists in the database"""
#         self.cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = %s", (user_id,))
#         return self.cursor.fetchone()[0] > 0

#     def bulk_insert_users(self, users):
#         """Insert new users, skipping existing ones"""
#         insert_query = """
#         INSERT INTO users (user_id, First_name, Last_name, personal_email, phone, Password_hash, profile_picture, created_date, modified_date)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
#         """
#         new_users = [user.to_tuple() for user in users if not self.user_exists(user.user_id)]
        
#         if new_users:
#             try:
#                 self.cursor.executemany(insert_query, new_users)
#                 self.db_connection.commit()
#                 print(f"Inserted {self.cursor.rowcount} new users")
#             except Exception as e:
#                 print(f"Error inserting users: {e}")
#         else:
#             print("No new users to insert.")

#     def close_connection(self):
#         """Close database connection"""
#         if self.db_connection:
#             self.db_connection.close()


# services/user_services.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db_connection import DatabaseConnection
from models.users import User  # Import the User class

class UserServices:
    def __init__(self):
        self.db_connection = DatabaseConnection().connect()
        self.cursor = self.db_connection.cursor()

    def user_exists(self, user_id):
        """Check if a user exists in the database"""
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0] > 0

    def bulk_insert_users(self, users):
        """Insert new users, skipping existing ones"""
        insert_query = """
        INSERT INTO users (user_id, first_name, last_name, personal_email, phone, Password_hash, profile_picture, created_date, modified_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        # Insert only new users (those that don't already exist)
        new_users = [user.to_tuple() for user in users if not self.user_exists(user.user_id)]

        if new_users:
            try:
                self.cursor.executemany(insert_query, new_users)
                self.db_connection.commit()
                print(f"Inserted {self.cursor.rowcount} new users")
            except Exception as e:
                print(f"Error inserting users: {e}")
        else:
            print("No new users to insert.")

    def close_connection(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()

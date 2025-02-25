# services/user_services.py
import sys
import os
from datetime import datetime

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

    def update_user(self, user):
        """Update an existing user (only modified_date will be updated)"""
        # Ensure that only modified_date is updated while preserving created_date
        update_query = """
        UPDATE users
        SET first_name = %s, last_name = %s, personal_email = %s, phone = %s, Password_hash = %s, profile_picture = %s, modified_date = NOW()
        WHERE user_id = %s
        """
        self.cursor.execute(update_query, (
            user.first_name, user.last_name, user.personal_email, user.phone, user.password_hash, user.profile_picture, user.user_id
        ))
        self.db_connection.commit()

    def delete_user(self, user_id):
        """Delete a user"""
        delete_query = "DELETE FROM users WHERE user_id = %s"
        self.cursor.execute(delete_query, (user_id,))
        self.db_connection.commit()

    def get_user_by_id(self, user_id):
        """Get a user by their ID"""
        self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(*row)  # Assuming your User model can handle this
        return None

    def get_all_users(self):
        """Get all users"""
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        # print("rows", rows,"\n")  # Print raw rows from DB
    
        # abc = []
        # for row in rows:
        #     print(f"Row data: {row}\n")  # Check row data before converting to User object
        #     user = User(*row)  # Create a User object
        #     print(f"User created: ID={user.user_id}, Name={user.first_name} {user.last_name}")  # Check the created user
        #     abc.append(user)
        #     print("user",user)

        # print("abc",abc)
        return [User(*row) for row in rows]  # Convert each row into a User object

    def close_connection(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()

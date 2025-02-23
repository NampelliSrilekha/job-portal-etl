# models/users.py
class User:
    def __init__(self, user_id, first_name, last_name, personal_email, phone, Password_hash, profile_picture=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.personal_email = personal_email
        self.phone = phone
        self.password_hash = Password_hash
        self.profile_picture = profile_picture

    def to_tuple(self):
        return (self.user_id, self.first_name, self.last_name, self.personal_email, self.phone, self.password_hash, self.profile_picture)

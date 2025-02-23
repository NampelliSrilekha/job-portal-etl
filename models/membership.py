# models/membership.py
class Membership:
    def __init__(self, membership_id, user_id, Type_of_membership, active_date, expiry_date):
        self.membership_id = membership_id
        self.user_id = user_id
        self.type_of_membership = Type_of_membership
        self.active_date = active_date
        self.expiry_date = expiry_date


    def to_tuple(self):
        return (self.membership_id, self.user_id, self.type_of_membership, self.active_date, self.expiry_date)

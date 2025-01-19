
class User:
    def __init__(self, username, password, is_admin=False, tickets=None):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.tickets = tickets if tickets else []

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "tickets": self.tickets,
            "is_admin": self.is_admin
        }

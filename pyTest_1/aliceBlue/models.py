
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = id
        self.password = "111"
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


from flask_login import UserMixin

# Ticket Users
class User(UserMixin):

    def __init__(
        self,
        p_Id,
        p_Username,
        p_Password):

        self.Id = p_Id
        self.Username = p_Username
        self.Password = p_Password

    def __repr__(self):
        return "%d/%s" % (self.Id, self.Username)

    def is_active(self):
        return not self.locked

    def get_id(self):
        return self.Username

    def is_authenticated(self):
        return True

    def is_anonymouse(self):
        return False

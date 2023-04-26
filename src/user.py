from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, username: str, id: int):

        self.username = username

        self.id = str(id)

    def get_id(self):
        return self.id
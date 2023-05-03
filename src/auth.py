import bcrypt
from src.user import User
from src.database import Database

def auth_user(username: str, password: str):

    with Database() as DB:
        user_info = DB.get_user_info(username)

        if user_info:
            if bcrypt.checkpw(password.encode("utf-8"), user_info[1].encode("utf-8")):
                return User(user_info[0], int(user_info[2]))
        return None

def add_user(username: str, password: str):

    hashpass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    with Database() as DB:
        DB.add_user(username, hashpass.decode())
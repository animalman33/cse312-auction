import bcrypt
from src.user import User
from src.userdb import UserDB


def auth_user(username: str, password: str):

    with UserDB() as DB:
        user_info = DB.get_user_info(username)

        if user_info:
            if bcrypt.checkpw(password.encode("utf-8"), user_info[1].encode("utf-8")):
                return User(user_info[0], int(user_info[2]))
        return None


def add_user(username: str, password: str):

    hashpass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    with UserDB() as DB:
        DB.add_user(username, hashpass.decode())

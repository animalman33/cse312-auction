from flask import Flask, render_template, redirect, request
from src.userdb import UserDB
from flask_login import LoginManager, login_required
import flask_login
from src.user import User
from src.auth import *
import secrets

app = Flask(__name__)

secret_key = secrets.token_urlsafe()
app.secret_key = secret_key

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def user_loader(id):
    with UserDB() as DB:
        user = DB.get_user_id(id)
        if user:
            return User(user[0], int(user[2]))
        return None

@app.route("/login", methods=["POST"])
def login_user():
    data = request.form

    username = data["username"]
    password = data["password"]

    user_obj = auth_user(username, password)
    if user_obj:
        flask_login.login_user(user_obj, remember=True)
        return redirect("/home")
    else:
        return redirect("/")

@app.route("/create/acc", methods=["POST"])
def create_acc():
    data = request.form
    username = data["username"]
    password = data["password"]

    add_user(username, password)

    return redirect("/")

@app.route("/home")
@login_required
def tmp():
    return render_template("index.html")

@app.route("/")
def hello_world():
    return render_template("index.html")

if __name__ == "__main__":
    UserDB().setup()

    app.run("0.0.0.0", port=8080, debug=True)

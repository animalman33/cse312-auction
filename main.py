from flask import Flask, abort, render_template, redirect, request, jsonify
from src.database import Database
from flask_login import LoginManager, current_user, login_required
import flask_login
from src.user import User
from src.auth import *
import secrets

app = Flask(__name__)

secret_key = secrets.token_urlsafe()
app.secret_key = secret_key

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "/login"

@login_manager.user_loader
def user_loader(id):
    with Database() as DB:
        user = DB.get_user_id(id)
        if user:
            return User(user[0], int(user[2]))
        return None

@app.errorhandler(404)
def return_404(_):
    return render_template("404.html"), 404

@app.route("/login", methods=["POST"])
def login_user():
    data = request.form

    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return redirect("/login")

    user_obj = auth_user(username, password)
    if user_obj:
        flask_login.login_user(user_obj, remember=True)
        return redirect("/user/home")
    else:
        return redirect("/login")


@app.route("/create/acc", methods=["POST"])
def create_acc():
    data = request.form

    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return redirect("/create/acc")

    add_user(username, password)

    return redirect("/login")

@app.route("/user/bids")
@login_required
def get_user_bids():

    with Database() as DB:
        info = DB.get_user_bids(current_user.get_id())
        return jsonify(info)

@app.route("/user/wins")
@login_required
def get_user_wins():

    with Database() as DB:

        data = DB.get_user_wins(current_user.get_id())

        return jsonify(data)

@app.route("/user/auc")
@login_required
def get_user_auc():
    with Database() as DB:

        data = DB.get_user_auc(current_user.get_id())

        return jsonify(data)

@app.route("/auc/create", methods=["POST"])
@login_required
def create_auc():

    form = request.form
    image = request.files

    with Database() as DB:
        name = form.get("name")
        cost = form.get("cost")
        auc_image = image.get("auc_image")
        userid = current_user.get_id()
        if name is None or cost is None or auc_image is None:
            return abort(400)
        with Database() as DB:
            check = DB.add_auc(userid, name, cost)
            if check is None:
                return abort(409)
    return abort(404)

@app.route("/auc/list")
@login_required
def list_aucs():
    with Database() as DB:
        data = DB.get_auc_list()
        return jsonify(data)

@app.route("/auc/<int:id>")
@login_required
def get_auc(id):

    with Database() as DB:
        data = DB.get_auc(id)
        if data:
            return render_template("auc.html")
    return abort(404)


@app.route("/user/home")
@login_required
def home_page():
    return render_template("home.html")

@app.route("/")
def initial_page():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/create/acc")
def create_acc_page():
    return render_template("create_acc.html")

if __name__ == "__main__":
    Database().setup()

    app.run("0.0.0.0", port=8080, debug=True)

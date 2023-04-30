from flask import Flask, abort, render_template, redirect, request, jsonify
from src.database import Database
import math
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
def return_404(e):
    return render_template("404.html"), 404

@app.route("/login", methods=["POST"])
def login_user():
    data = request.form

    username = data["username"]
    password = data["password"]

    user_obj = auth_user(username, password)
    if user_obj:
        flask_login.login_user(user_obj, remember=True)
        return redirect("/user/home")
    else:
        return redirect("/login")

@app.route("/login")
def login_page():
    return render_template("index.html")

@app.route("/create/acc", methods=["POST"])
def create_acc():
    data = request.form
    username = data["username"]
    password = data["password"]

    add_user(username, password)

    return redirect("/login")

@app.route("/user/add/bid", method=["POST"])
@login_required
def add_user_bid():
    """
    this function is called on post for route '/user/add/bid'
    it expects a json message of format
    {
    'auc_id': id<int>,
    'amount': amount<int>
    }

    send a json message of {'status': 0} if it succeeded
    otherwise send {'status': 1} if the amount is less than the current bid or if the auctions does not exist
    """
    data = request.get_json()
    if data:
        amount = data.get('amount')
        auc_id = data.get('auc_id')
        if amount is None or auc_id is None:
            return abort(400)
        with Database() as DB:
            if(DB.add_bid(math.floor(amount), auc_id, current_user.get_id())):
                return jsonify({"status": 0}, success=True)
            else:
                return jsonify({'status': 1})
    else:
        return abort(415)


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


@app.route("/user/home")
@login_required
def home_page():
    return render_template("home.html")

@app.route("/")
def initial_page():
    return render_template("index.html")


if __name__ == "__main__":
    Database().setup()

    app.run("0.0.0.0", port=8080, debug=True)

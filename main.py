from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user
from src.userdb import UserDB
from src.user import User
# import socketio
from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)
socketio.run(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Get session user
@login_manager.user_loader
def user_loader(id):
    with UserDB() as DB:
        user = DB.get_user_id(id)
        if user:
            return User(user[0], int(user[2]))
        return None

user = user_loader(id)

# Redirects non-users to login
@login_manager.unauthorized_handler
def unauthorized():
    if user == None:
        return redirect("/login")
    else:
        pass

# Render page
@app.route('/')
def index():
    return render_template('index.html')

# Join a auction room
@socketio.on('join')
def join_auction(user):
    username = user['username']
    auction_room = user['room']
    join_room(auction_room)
    send(username + ' has joined.', to=auction_room)

# Leave a auction room
@socketio.on('leave')
def leave_auction(user):
    username = user['username']
    auction_room = user['room']
    leave_room(auction_room)
    send(username + ' has left.', to=auction_room)

# See new bids
@socketio.on('bid')
def new_bid(json):
    print("Bid" + str(json))

# Send a bid
@socketio.on('bid')
def handle_bid(json):
    send(json)

# @app.route("/auctions/<int:auction_id>", methods=["POST"])
# def AuctionConnection():
#     users = []

# @app.websocket('/websocket')
# def Auction(websocket: SocketIO):
#     while True:

if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)
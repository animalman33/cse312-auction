from flask import Flask, render_template, redirect, session, request
from flask_login import LoginManager, current_user
from src.database import Database
from src.user import User
from flask_socketio import SocketIO, join_room, leave_room, rooms, emit, send, broadcast
from main import *

app = Flask(__name__)
socketio = SocketIO(app)

users = {}

# Join a auction room
@socketio.on('join_auction')
@current_user
def join_auction(user, auctionID):
    users[user] = request.sid
    join_room(auctionID)
    send("You have entered!", to=auctionID)
    emit("feed", {user} + ' has joined.', broadcast=True)

# Create a auction
@socketio.on('create_auction')
@current_user
def create_auction(user, price, name):
    # Gets the user based off session ID
    username = None
    for user in users:
        if users[user] == request.sid:
            username = user
    Database.add_auc(username, Database.get_user_info(username)[2], name, price)

# Leave a auction room
@socketio.on('leave')
@current_user
def leave_auction(user, auctionID):
    leave_room(auctionID)
    send("You have left!", to="/user/home")
    emit("feed", {user} + ' has left.', broadcast=True)

# Send a bid
@socketio.on('new_bid')
@current_user
def new_bid(amount):
    # Gets the user based off session ID
    username = None
    for user in users:
        if users[user] == request.sid:
            username = user
    # Add bid and send to feed
    Database.add_bid(username, amount, rooms(request.sid), Database.get_user_info(username)[2])
    emit("feed", {username} + ' has bid ' + {str(amount)}, broadcast=True)

if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)
    socketio.run(app)
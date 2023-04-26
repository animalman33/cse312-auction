from flask import Flask, render_template, request
# from flask_login import current_user   
# import socketio
from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def join_auction(user):
    username = user['username']
    auction_room = user['room']
    join_room(auction_room)
    send(username + ' has joined.', to=auction_room)

@socketio.on('leave')
def leave_auction(user):
    username = user['username']
    auction_room = user['room']
    leave_room(auction_room)
    send(username + ' has left.', to=auction_room)

@socketio.on('bid')
def new_bid(json):
    print("Bid" + str(json))

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
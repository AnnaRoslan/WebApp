from flask import Flask, Response, request
from flask_cors import CORS
from flask_socketio import SocketIO, join_room,leave_room, emit
from jwt import decode

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

cors = CORS(app, resources={r"/*": {"origins": "*"}})

ROOM_ID = "room_id"
MESSAGE = "message"


@app.route("/", methods=["GET"])
def main():
    return Response(status=200)

@socket_io.on("connect")
def handle_on_connect():
    room = request.args.get('room')
    join_room(room)

@socket_io.on("leave")
def handle_on_leave(data):
    room_id = data[ROOM_ID]
    leave_room(room_id)
    
@socket_io.on("join")
def handle_on_join(data):
    room_id = data[ROOM_ID]
    join_room(room_id)
    emit("joined_room", {"room_id": room_id})

@app.route("/send", methods=["POST"])
def send_notification():
    user_login = request.get_json(force=True)["userLogin"]
    message = request.get_json(force=True)["message"]

    socket_io.emit("send_my_message", {MESSAGE: message}, room=user_login)

    return Response(status=200)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
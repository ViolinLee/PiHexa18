import threading
from flask import Flask, render_template
from flask_socketio import SocketIO
from movement import MovementMode


app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('command')
def handle_command(data):
    req_mode = data['mode']
    FlaskRemote.mode = MovementMode.get_value(req_mode)
    print(f"Received command {req_mode} from client, parsing to mode enum value: {FlaskRemote.mode}")


class FlaskRemote(threading.Thread):
    mode = MovementMode.MOVEMENT_STANDBY.value

    def __init__(self, auto_start=True):
        super().__init__(daemon=False)

        if auto_start:
            self.start()

    def run(self) -> None:
        socketio.run(app, debug=False)


if __name__ == '__main__':
    remote = FlaskRemote()
    print("If the code runs to here, it means FlaskRemote() non-blocking.(Can be controlled using 'daemon' arg)")

from btpycom import *
from movement import MovementMode


class Remote(object):
    def __init__(self, service_name='PiHexa BTServer', is_verbose=False):
        self.bt_server = BTServer(service_name, self.on_state_changed, is_verbose)
        self.mode = 0

    def on_state_changed(self, state, msg):
        if state == "LISTENING":
            print("Listening", msg)
        elif state == "CONNECTED":
            print("Connected", msg)
        elif state == "MESSAGE":
            print("Message", msg)
            if msg == 'RotateX':
                self.mode = MovementMode.MOVEMENT_ROTATEX.value
            elif msg == 'RotateY':
                self.mode = MovementMode.MOVEMENT_ROTATEY.value
            elif msg == 'RotateZ':
                self.mode = MovementMode.MOVEMENT_ROTATEZ.value
            elif msg == 'Twist':
                self.mode = MovementMode.MOVEMENT_TWIST.value
            elif msg == 'TurnLeft':
                self.mode = MovementMode.MOVEMENT_TURNLEFT.value
            elif msg == 'TurnRight':
                self.mode = MovementMode.MOVEMENT_TURNRIGHT.value
            elif msg == 'Run':
                self.mode = MovementMode.MOVEMENT_FORWARDFAST.value
            elif msg == 'Forward':
                self.mode = MovementMode.MOVEMENT_FORWARD.value
            elif msg == 'Climb':
                self.mode = MovementMode.MOVEMENT_CLIMB.value
            elif msg == 'ShiftLeft':
                self.mode = MovementMode.MOVEMENT_SHIFTLEFT.value
            elif msg == 'ShiftRight':
                self.mode = MovementMode.MOVEMENT_SHIFTRIGHT.value
            elif msg == 'Backward':
                self.mode = MovementMode.MOVEMENT_BACKWARD.value
            else:
                pass
        elif state == "DISCONNECTED":
            print("Disconnected", msg)
        else:
            raise ValueError

    def disconnect(self):
        self.bt_server.disconnect()

    def send_msg(self, msg):
        self.bt_server.sendMessage(msg)

    def is_connected(self):
        return self.bt_server.isClientConnected

    def is_terminated(self):
        return self.bt_server.isServerRunning


if __name__ == '__main__':
    remote = Remote()

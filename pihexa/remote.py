from btpycom import *
from movement import MovementMode


class Remote(object):
    def __init__(self, service_name='PiHexa BTServer', is_verbose=False):
        self.bt_server = BTServer(service_name, self.on_state_changed, is_verbose)
        self.mode = MovementMode.MOVEMENT_STANDBY.value

    def on_state_changed(self, state, msg):
        if state == "LISTENING":
            print("Listening", msg)
        elif state == "CONNECTED":
            print("Connected", msg)
        elif state == "MESSAGE":
            print("Message", msg)
            if msg == "bytearray(b'Standby')":
                self.mode = MovementMode.MOVEMENT_STANDBY.value
            elif msg == "bytearray(b'RotateX')":
                self.mode = MovementMode.MOVEMENT_ROTATEX.value
            elif msg == "bytearray(b'RotateY')":
                self.mode = MovementMode.MOVEMENT_ROTATEY.value
            elif msg == "bytearray(b'RotateZ')":
                self.mode = MovementMode.MOVEMENT_ROTATEZ.value
            elif msg == "bytearray(b'Twist')":
                self.mode = MovementMode.MOVEMENT_TWIST.value
            elif msg == "bytearray(b'TurnLeft')":
                self.mode = MovementMode.MOVEMENT_TURNLEFT.value
            elif msg == "bytearray(b'TurnRight')":
                self.mode = MovementMode.MOVEMENT_TURNRIGHT.value
            elif msg == "bytearray(b'Run')":
                self.mode = MovementMode.MOVEMENT_FORWARDFAST.value
            elif msg == "bytearray(b'Forward')":
                self.mode = MovementMode.MOVEMENT_FORWARD.value
            elif msg == "bytearray(b'Climb')":
                self.mode = MovementMode.MOVEMENT_CLIMB.value
            elif msg == "bytearray(b'ShiftLeft')":
                self.mode = MovementMode.MOVEMENT_SHIFTLEFT.value
            elif msg == "bytearray(b'ShiftRight')":
                self.mode = MovementMode.MOVEMENT_SHIFTRIGHT.value
            elif msg == "bytearray(b'Backward')":
                self.mode = MovementMode.MOVEMENT_BACKWARD.value
            else:
                pass
        elif state == "DISCONNECTED":
            print("Disconnected", msg)
        else:
            raise ValueError

    def reset_standby_mode(self):
        self.mode = MovementMode.MOVEMENT_STANDBY.value

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

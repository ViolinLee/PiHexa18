from btpycom import *


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
            if msg in [str(num) for num in range(14)]:  # mode
                self.mode = int(msg)
            else:
                raise ValueError
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

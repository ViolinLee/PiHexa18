import socket
import threading
import re
import time
from movement import MovementMode


class WebRemote:
    def __init__(self, auto_start=True):
        self.mode = MovementMode.MOVEMENT_STANDBY.value
        self.url_path = r"/api/remote/(.*)"

        if auto_start:
            self.begin()

    def handle_request(self, client_socket):
        request_data = client_socket.recv(1024).decode()

        # 解析HTTP请求
        request_lines = request_data.split('\r\n')
        method, path, version = request_lines[0].split()

        match = re.match(self.url_path, path)
        if match:
            req_mode = match.group(1)
            try:
                self.mode = MovementMode.get_value(req_mode)
                print(f"Update mode: {self.mode}")
            except ValueError as e:
                print("Error:", str(e))

        # 构造HTTP响应
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        response += f"<h1>Welcome to PiHexa18's Web-API!</h1>"
        response += f"<p>Mode: {self.mode}</p >"

        # 发送HTTP响应 & 关闭客户端连接
        client_socket.sendall(response.encode())
        client_socket.close()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 8080))
        server_socket.listen(2)

        while True:
            client_socket, addr = server_socket.accept()
            self.handle_request(client_socket)

    def begin(self):
        client_thread = threading.Thread(target=self.start_server, args=())
        client_thread.start()

    def reset_standby_mode(self):
        self.mode = MovementMode.MOVEMENT_STANDBY.value

    def is_connected(self):
        return True


if __name__ == '__main__':
    my_class_instance = WebRemote()

    print("Server started!")
    while True:
        time.sleep(2)
        pass

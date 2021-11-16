import subprocess
from time import sleep
from socket import socket, gethostname, gethostbyname, SOL_SOCKET, SO_REUSEADDR, AF_INET, SOCK_STREAM


def is_wlan_connected():
    # Check if wlan connected. Work on linux platform
    ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        output_wlan_list = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
        is_connected = True
        print(output_wlan_list)
    except subprocess.CalledProcessError:
        is_connected = False
        print("No wireless networks connected")
    return is_connected


def web_callback(leg_calibrator):
    # Wait for WIFI connection
    while not is_wlan_connected():
        sleep(2)

    # Get STA IP
    sta_ip = gethostbyname(gethostname())
    print('PiHexa IP: ', sta_ip)

    # Setup Socket WebServer
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((sta_ip, 80))
    s.listen(2)

    # Main Loop
    while True:
        # Accept request from clients
        conn, addr = s.accept()
        # req = str(conn.recv(1024))
        req = conn.recv(1024).decode()
        # conn.sendall('HTTP/1.1 200 OK\nConnection: close\nServer: FireBeetle\nContent-Type: text/html\n\n')
        if req.find('favicon.ico') > -1:  # Filter
            conn.close()
            continue

        # Parse Request and Process Remote Control Panel Input from Client
        leg_calibrator.process_panel(req)

        # Response and Close Socket
        conn.sendall(leg_calibrator.panel_html)
        conn.close()


class Calibrator:
    def __init__(self):
        self.panel_html = 'html'
        self.calibrating = False
        self.data = [0] * 18

    def process_panel(self, panel_req):
        # update data
        if 'GET /?MODE=TrotGait' in panel_req:
            self.calibrating = True
        if 'GET /?MODE=SAVE' in panel_req:
            self.calibrating = False

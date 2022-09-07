import subprocess
from time import sleep
from socket import socket, gethostname, gethostbyname, SOL_SOCKET, SO_REUSEADDR, AF_INET, SOCK_STREAM
from config import html_bytes


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
    sta_ip = gethostbyname(gethostname() + '.local')
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
    def __init__(self, initial_data):
        self.panel_html = html_bytes
        self.calibrating = False
        self.data = initial_data

    def process_panel(self, panel_req):
        start_tag = 'GET /start'
        finish_tag = 'GET /finish'
        cali_tag = 'GET /calibration='

        if start_tag in panel_req:
            self.calibrating = True
        elif finish_tag in panel_req:
            self.calibrating = False
        elif cali_tag in panel_req:  # update data
            index = panel_req.find(cali_tag)
            req_data = [int(str_num) for str_num in panel_req[index + len(cali_tag):].split()[0].split(',')]

            temp = [req_data[3 * i: 3 * i + 3] for i in range(6) if i % 2 == 1]
            temp_r = [req_data[3 * i: 3 * i + 3] for i in range(6) if i % 2 == 0]
            temp_r.reverse()
            calibration_data = temp + temp_r

            self.data = calibration_data
        else:
            pass

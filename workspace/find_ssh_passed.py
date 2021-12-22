import paramiko
import _thread
import sys
import time
from tqdm import tqdm


def connect(host_str):
    try:
        transport = paramiko.Transport((host_str, port))
        # transport.connect(username='pi', password='raspberry')
        # transport.connect(username=user, password=pwd)
    except:
        return
    else:
        print(host_str)


def find_ip(ip_prefix):
    for i in tqdm(range(1, 256)):
        ip = '%s.%s' % (ip_prefix, i)

        _thread.start_new_thread(connect, (ip,))
        time.sleep(0.3)


if __name__ == '__main__':
    print("start time %s" % time.ctime())

    port = 22
    user = 'pi'
    password = 'raspberry'

    commandargs = sys.argv[1:]
    args = "".join(commandargs)

    ip_prefix = '.'.join(args.split('.')[:-1])
    find_ip(ip_prefix)
    print("end time %s" % time.ctime())

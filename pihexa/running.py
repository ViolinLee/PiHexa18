# -*- coding: utf-8 -*-

import _thread
from time import time, sleep
from hexapod import Hexapod
from remote import Remote
from web_calibrator import Calibrator, web_callback
from config import movement_interval, calibration_path


DEBUG = False
REACT_DELAY = movement_interval * 0.001
loop_mode = 1  # default normal-loop


def normal_loop():
    if not remote.is_connected():
        sleep(1 - REACT_DELAY)

    t0 = time()
    pi_hexa.process_movement(remote.mode, REACT_DELAY)
    time_spent = time() - t0
    if time_spent < REACT_DELAY:
        sleep(REACT_DELAY - time_spent)
    elif DEBUG:
        print(time_spent)
    else:
        pass


def calibrating_loop():
    while calibrator.calibrating is True:
        pi_hexa.process_calibration(calibrator.data)  # 动作同时将calibration信息保存在pi_hexa私有变量
    pi_hexa.save_calibration(calibration_path)


if __name__ == '__main__':
    # Remote controller instance (BTCOM)
    remote = Remote()

    # Hexapod instance
    pi_hexa = Hexapod()
    pi_hexa.init()

    # WEB calibrator instance (WLAN STA)
    calibrator = Calibrator(pi_hexa.leg_servo.offset)
    _thread.start_new_thread(web_callback, (calibrator, ))

    while True:
        if calibrator.calibrating is True:
            calibrating_loop()
        else:
            normal_loop()

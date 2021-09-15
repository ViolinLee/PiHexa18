import os
import argparse
from hexapod import hexapod
from time import time, sleep
from .config import movement_interval, calibration_path


react_delay = movement_interval * 0.001


def normal_loop():
    if not remote.connected():
        sleep(1 - react_delay)

    t0 = time()
    remote.process()
    mode = remote.mode

    pi_hexa.process_movement(mode, react_delay)
    time_spent = time() - t0
    if time_spent < react_delay:
        sleep(react_delay - time_spent)
    else:
        print(time_spent)


def calibrating_loop(path):
    # json file
    with open(path, 'w') as f:

        pass
    return


def anamating_loop():
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default=2, help="Action mode: 0-calibration 1-normal running 2-animation")
    parser.parse_args()

    mode = 0
    # Remote controller instance
    remote = remote()

    # Hexapod instance
    pi_hexa = hexapod.Hexapod()
    pi_hexa.init()

    if mode == 0:
        calibrating_loop(calibration_path)
    elif mode == 1:
        while True:
            normal_loop()
    else:
        animating_loop()

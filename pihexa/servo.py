# -*- coding: utf-8 -*-

from pca9685 import PCA9685


class Servo(object):
    def __init__(self, left_address=0x41, right_address=0x40):
        self.pwm_left = PCA9685(left_address)
        self.pwm_right = PCA9685(right_address)

    def set_angle(self, leg_index, part_index, angles):
        return


if __name__ == '__main__':
    servo1 = Servo(1, 2)

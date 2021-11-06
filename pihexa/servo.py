# -*- coding: utf-8 -*-

from pca9685 import PCA9685
from numpy import interp


class Servo(object):
    def __init__(self, offset_array=None, left_address=0x41, right_address=0x40, pulse_min=544, pulse_max=2400):
        if offset_array is None:
            offset_array = [0] * 18
        self.pwm_left = PCA9685(left_address)
        self.pwm_right = PCA9685(right_address)
        self.pulse_min = pulse_min
        self.pulse_max = pulse_max
        self.pulse_middle = (self.pulse_min + self.pulse_max) / 2
        self.offset_array = offset_array

    def angle2pulse(self, angle):
        # 注意运动学定义的0°对应舵机90°位置
        return self.pulse_middle + interp(angle, [0, 180], [self.pulse_min, self.pulse_max])

    def set_angle(self, leg_index, part_index, angle):
        # switch left, right pwm
        if leg_index == 0:
            pwm_index = 5 + part_index
            pwm = self.pwm_left
        elif leg_index == 1:
            pwm_index = 2 + part_index
            pwm = self.pwm_left
        elif leg_index == 2:
            pwm_index = 8 + part_index
            pwm = self.pwm_left
        elif leg_index == 3:
            pwm_index = 8 + part_index
            pwm = self.pwm_left
        elif leg_index == 4:
            pwm_index = 2 + part_index
            pwm = self.pwm_left
        elif leg_index == 5:
            pwm_index = 5 + part_index
            pwm = self.pwm_left
        else:
            raise ValueError

        inverse = True if part_index == 1 else False
        correct = -1 if inverse else 1

        pulse = correct * self.angle2pulse(angle) + self.offset_array[leg_index][part_index]
        pwm.setServoPulse(pwm_index, pulse)


if __name__ == '__main__':
    servo1 = Servo(1, 2)

# -*- coding: utf-8 -*-


class Servo(object):
    def __init__(self, leg_index, part_index):
        self.leg_index = leg_index
        self.part_index = part_index
        self.pwm_inited = False

    def set_angle(self, angles):
        return

    def init_PWM(self):
        if self.pwm_inited:
            return

    def init(self):
        self.init_PWM()


if __name__ == '__main__':
    servo1 = Servo(1, 2)

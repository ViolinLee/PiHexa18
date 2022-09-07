# -*- coding: utf-8 -*-

from pca9685 import PCA9685
# from numpy import interp


class Servo(object):
    def __init__(self, left_address=0x40, right_address=0x41, pulse_min=544, pulse_max=2400, freq=50):
        self.offset = [[0, 0, 0]] * 6
        self.pwm_left = PCA9685(left_address)
        self.pwm_right = PCA9685(right_address)
        self.pulse_min = pulse_min
        self.pulse_max = pulse_max
        self.pulse_middle = (self.pulse_min + self.pulse_max) / 2

        # Set pwm frequency
        self.pwm_left.setPWMFreq(freq)
        self.pwm_right.setPWMFreq(freq)

    def angle2pulse(self, km_angle, reverse):
        # return interp(correct * km_angle, [-90, 90], [pulse_min, pulse_max])  # 注意运动学定义的0°对应舵机90°位置
        return (self.pulse_min + self.pulse_max) / 2 + reverse * km_angle * ((self.pulse_max - self.pulse_min) / 180)

    def set_offset(self, offset):
        self.offset = offset

    def set_angle(self, leg_index, part_index, km_angle):
        # switch left, right pwm
        if leg_index == 0:
            pwm_index = 5 + part_index
            pwm = self.pwm_right
        elif leg_index == 1:
            pwm_index = 2 + part_index
            pwm = self.pwm_right
        elif leg_index == 2:
            pwm_index = 8 + part_index
            pwm = self.pwm_right
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

        km_angle_corrected = km_angle + self.offset[leg_index][part_index]
        inverse = -1 if part_index == 1 else 1
        pulse = self.angle2pulse(km_angle_corrected, inverse)
        pwm.setServoPulse(pwm_index, pulse)


if __name__ == '__main__':
    from time import sleep

    servo = Servo()
    while True:
        for angle in range(-90, 91):
            for leg_i in range(6):
                for part_j in range(3):
                    servo.set_angle(leg_i, part_j, angle)
            sleep(0.02)
        for angle in range(90, -91, -1):
            for leg_i in range(6):
                for part_j in range(3):
                    servo.set_angle(leg_i, part_j, angle)
            sleep(0.02)

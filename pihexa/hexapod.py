# -*- coding: utf-8 -*-

# from servo import Servo
from movement import Movement, MovementMode
from leg import Leg
from config import *


class Hexapod(object):
    def __init__(self):
        self.__legs = [Leg(i) for i in range(6)]
        self.__movement = Movement(MovementMode.MOVEMENT_STANDBY)
        self.__mode = MovementMode.MOVEMENT_STANDBY

    def init(self, setting):
        self.init_pwm()

        # LFlash.begin()
        # calibrationLoad()

        if not setting:
            self.process_movement(MovementMode.MOVEMENT_STANDBY)

    def process_movement(self, mode, elapsed=0):  # 重要函数，与步态执行有关
        if self.__mode != mode:
            self.__mode = mode
            self.__movement.set_mode(self.__mode)

        location = self.__movement.next(elapsed=elapsed)
        for i in range(6):
            self.__legs[i].move_tip(location.get(i))


class VirtualHexapod(object):
    def __init__(self, ax, origin=(0, 0, 0), initial_height=stanby_z):
        self.ax = ax
        self.initial_height = initial_height
        self.__legs = [Leg(i) for i in range(6)]
        self.body_vector = [(origin[0] + leg_mount_other_x, origin[1] + leg_mount_other_y, origin[2]),
                            (origin[0] + leg_mount_left_right_x, origin[1], origin[2]),
                            (origin[0] + leg_mount_other_x, origin[1] - leg_mount_other_y, origin[2]),
                            (origin[0] - leg_mount_other_x, origin[1] - leg_mount_other_y, origin[2]),
                            (origin[0] - leg_mount_left_right_x, origin[1], origin[2]),
                            (origin[0] - leg_mount_other_x, origin[1] + leg_mount_other_y, origin[2]),
                            (origin[0] + leg_mount_other_x, origin[1] + leg_mount_other_y, origin[2])]
        self.leg_vector = []

    def draw_body(self, color='black'):
        x_data = [vector[0] for vector in self.body_vector]
        y_data = [vector[1] for vector in self.body_vector]
        z_data = [vector[2] for vector in self.body_vector]
        self.ax.plot(x_data, y_data, z_data, color=color)

    def draw_legs(self, color='blue'):

        return
# -*- coding: utf-8 -*-

from servo import *
from movement import *


class Hexapod(object):
    def __init__(self):
        self.__legs = [0, 1, 2, 3, 4, 5]
        self.__movement = Movement(MovementMode.MOVEMENT_STANDBY)
        self.__mode = MovementMode.MOVEMENT_STANDBY

    def init(self, setting):
        Servo.init_PWM()

        # LFlash.begin()
        # calibrationLoad()

        if not setting:
            self.process_movement(MovementMode.MOVEMENT_STANDBY)

    def process_movement(self, mode, elapsed):
        if self.__mode != mode:
            self.__mode = mode
            self.__movement.set_mode(self.__mode)

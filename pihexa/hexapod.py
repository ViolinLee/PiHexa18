# -*- coding: utf-8 -*-

# from servo import Servo
from movement import Movement, MovementMode
from leg import Leg


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

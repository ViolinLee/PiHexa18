# -*- coding: utf-8 -*-

from enum import Enum
from base import *

"""
定义六足机器人移动相关函数。
"""


class MovementMode(Enum):
    MOVEMENT_STANDBY = 0

    MOVEMENT_FORWARD = 1
    MOVEMENT_FORWARDFAST = 2
    MOVEMENT_BACKWARD = 3
    MOVEMENT_TURNLEFT = 4
    MOVEMENT_TURNRIGHT = 5
    MOVEMENT_SHIFTLEFT = 6
    MOVEMENT_SHIFTRIGHT = 7
    MOVEMENT_CLIMB = 8
    MOVEMENT_ROTATEX = 9
    MOVEMENT_ROTATEY = 10
    MOVEMENT_ROTATEZ = 11
    MOVEMENT_TWIST = 12

    MOVEMENT_TOTAL = 13


class Movement(object):
    def __init__(self, mode: MovementMode):
        self.__mode = mode
        self.__position = locations()
        self.__index = 0
        self.__transiting = False
        self.__remain_time = 0

    def set_mode(self, new_mode):
        return




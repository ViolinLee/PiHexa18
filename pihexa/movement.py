# -*- coding: utf-8 -*-

from enum import Enum
from random import randint
from movement_table import *

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


k_table = [standby_table,
           forward_table,
           forward_fast_table,
           backward_table,
           turn_left_table,
           turn_right_table,
           shift_left_table,
           shift_right_table,
           climb_table,
           rotate_x_table,
           rotate_y_table,
           rotate_z_table,
           twist_table]


class Movement(object):
    def __init__(self, mode, transiting: bool):
        self.__mode = mode
        self.__position = locations()  # k_standby
        self.__index = 0  # index in mode position table
        self.__transiting = transiting  # if still in transiting to new mode
        self.__remain_time = 0

    def set_mode(self, new_mode):
        print(standby_table.entries)
        if not k_table[new_mode].entries:
            # log_info
            return

        self.__mode = new_mode

        table = k_table[self.__mode]

        self.__index = table.entries[randint(0, 255) % table.entries_count]  # count==2: __index = 0 or 1
        self.__remain_time = movement_switch_duration if movement_switch_duration > table.step_duration else table.step_duration  # maximum value

        print("movement.mode", self.__mode)

    def next(self, elapsed):
        table = k_table[self.__mode]

        if elapsed <= 0:
            elapsed = table.step_duration  # 使elapsed的值合理

        if self.__remain_time <= 0:  # 小于零，表示该步完成，则开始下一步（步的index自增1）
            self.__index = (self.__index + 1) % table.length  # index会循环取[0, table_length)的值
            self.__remain_time = table.step_duration

        if elapsed >= self.__remain_time:  # 仍剩最后一次迭代。过后，self.__position == table[self.__index]
            elapsed = self.__remain_time

        # 对每一步再细分（remain_time是前一步态途径点与后一步态途径点的间隔；step_duration是前一细分步与后一细分步的间隔）
        ratio = elapsed / self.__remain_time
        self.__position += (table.table[self.__index] - self.__position) * ratio
        self.__remain_time -= elapsed

        return self.__position




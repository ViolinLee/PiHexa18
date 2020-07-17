# -*- coding: utf-8 -*-

from base import *
from config import *
from math_utils import *
from hexapod import *
from servo import *
from math import sin, cos, pi, atan2, sqrt, acos
hpi = pi/2

"""
定义六足机器人单腿类，包括基坐标转换和正逆运动学相关类函数。
"""

class Leg(object):
    def __init__(self, leg_index):
        self.__leg_index = leg_index
        self.__servos = [Servo(self.__leg_index, i) for i in range(3)]
        self.__tip_pos = point3d()
        self.__tip_pos_local = point3d()

        """ 
        local_conv: 世界坐标系上的表达转换到本地坐标系上的表达
        world_conv: 本地坐标系上的表达转换到世界坐标系上的表达
        """
        if self.__leg_index == 0:  # 45 or -315 degree:
            self.__mount_position = point3d(leg_mount_other_x, leg_mount_other_y, 0)
            self.__local_conv = rotate315
            self.__world_conv = rotate45
        if self.__leg_index == 1:  # 0 degree:
            self.__mount_position = point3d(leg_mount_other_x, leg_mount_other_y, 0)
            self.__local_conv = rotate0
            self.__world_conv = rotate0
        if self.__leg_index == 2:  # -45 or 315 degree:
            self.__mount_position = point3d(leg_mount_other_x, leg_mount_other_y, 0)
            self.__local_conv = rotate45
            self.__world_conv = rotate315
        if self.__leg_index == 3:  # -135 or 225 degree:
            self.__mount_position = point3d(leg_mount_other_x, leg_mount_other_y, 0)
            self.__local_conv = rotate135
            self.__world_conv = rotate225
        if self.__leg_index == 4:  # -180 or 180 degree:
            self.__mount_position = point3d(leg_mount_other_x, leg_mount_other_y, 0)
            self.__local_conv = rotate180
            self.__world_conv = rotate180
        if self.__leg_index == 5:  # -225 or 135 degree:
            self.__mount_position = point3d(leg_mount_other_x, leg_mount_other_y, 0)
            self.__local_conv = rotate225
            self.__world_conv = rotate135


    """coordinate system translation"""
    def translate2local(self, world_point: point3d):
        return self.__local_conv(world_point - self.__mount_position)

    def translate2world(self, local_point: point3d):
        return self.__world_conv(local_point) + self.__mount_position

    def set_joint_angle(self, angles):
        out_point = self.__forward_kinematics(angles)
        self.move_tip_local(out_point)

    """word coordiante system (default)"""
    def move_tip(self, target_point_world: point3d):
        if target_point_world == self.__tip_pos:
            return
        dest_local = self.translate2local(target_point_world)
        # logging info
        self.__move(dest_local)
        self.__tip_pos = target_point_world
        self.__tip_pos_local = dest_local

    def get_tip_position(self):
        return self.__tip_pos

    """local coordinate system version"""
    def move_tip_local(self, target_point_local: point3d):
        if target_point_local == self.__tip_pos_local:
            return
        dest_world = self.translate2world(target_point_local)
        self.__move(target_point_local)
        self.__tip_pos = dest_world
        self.__tip_pos_local = target_point_local

    def get_tip_position_local(self):
        return self.__tip_pos_local

    """forward and inverse kinematics calculations are below local coordinate"""
    def __forward_kinematics(self, angles):
        radians = [angle * pi / 180 for angle in angles]
        x = leg_joint1_2joint2 + cos(radians[1]) * leg_joint2_2joint3 + cos(radians[1] + radians[2] - hpi) * leg_joint3_2tip

        out_point = point3d()
        out_point.x = leg_root2joint1 + cos(radians[0]) * x
        out_point.y = sin(radians[0]) * x
        out_point.z = sin(radians[1]) * leg_joint2_2joint3 + sin(radians[1] + radians[2] - hpi) * leg_joint3_2tip

        return out_point

    def __inverse_kinematics(self, target_point: point3d):
        angles = [0.0] * 3

        x = target_point.x
        y = target_point.y
        angles[0] = atan2(y, x) * 180 / pi

        x = sqrt(x**2 + y**2) - leg_joint1_2joint2
        y = target_point.z
        ar = atan2(y, x)
        lr2 = x**2 + y**2
        lr = sqrt(lr2)
        a1 = acos((lr2 + leg_joint2_2joint3**2 - leg_joint3_2tip**2) / (2 * leg_joint2_2joint3 * lr))
        a2 = acos((lr2 - leg_joint2_2joint3**2 + leg_joint3_2tip**2) / (2 * leg_joint3_2tip * lr))
        angles[1] = (ar + a1) * 180 / pi
        angles[2] = 90 - ((a1 + a2) * 180 / pi)

        return angles

    def __move(self, target_point):
        return

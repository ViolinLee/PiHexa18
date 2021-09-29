# -*- coding: utf-8 -*-

from config import *
from math_utils import *
from servo import *
from movement_const import *
from math import sin, cos, pi, atan2, sqrt, acos


hpi = pi/2


class Leg(object):
    """
    定义六足机器人单腿类，包括基坐标转换和正逆运动学相关类函数。
    """
    def __init__(self, leg_index):
        self.__leg_index = leg_index
        self.__servos = [Servo(self.__leg_index, i) for i in range(3)]

        """ 
        local_conv: 世界坐标系上的表达转换到本地坐标系上的表达
        world_conv: 本地坐标系上的表达转换到世界坐标系上的表达
        """
        if self.__leg_index == 0:  # 45 or -315 degree:
            self.__mount_position = point3d(leg_mount_other_x, leg_mount_other_y, 0)
            self.__local_conv = rotate315
            self.__world_conv = rotate45
            self.__tip_pos_local = point3d(p1_x, p1_y, p1_z)
            self.__tip_pos = self.translate2world(self.__tip_pos_local)
        elif self.__leg_index == 1:  # 0 degree:
            self.__mount_position = point3d(leg_mount_left_right_x, 0, 0)
            self.__local_conv = rotate0
            self.__world_conv = rotate0
            self.__tip_pos_local = point3d(p2_x, p2_y, p2_z)
            self.__tip_pos = self.translate2world(self.__tip_pos_local)
        elif self.__leg_index == 2:  # -45 or 315 degree:
            self.__mount_position = point3d(leg_mount_other_x, -leg_mount_other_y, 0)
            self.__local_conv = rotate45
            self.__world_conv = rotate315
            self.__tip_pos_local = point3d(p3_x, p3_y, p3_z)
            self.__tip_pos = self.translate2world(self.__tip_pos_local)
        elif self.__leg_index == 3:  # -135 or 225 degree:
            self.__mount_position = point3d(-leg_mount_other_x, -leg_mount_other_y, 0)
            self.__local_conv = rotate135
            self.__world_conv = rotate225
            self.__tip_pos_local = point3d(p4_x, p4_y, p4_z)
            self.__tip_pos = self.translate2world(self.__tip_pos_local)
        elif self.__leg_index == 4:  # -180 or 180 degree:
            self.__mount_position = point3d(-leg_mount_left_right_x, 0, 0)
            self.__local_conv = rotate180
            self.__world_conv = rotate180
            self.__tip_pos_local = point3d(p5_x, p5_y, p5_z)
            self.__tip_pos = self.translate2world(self.__tip_pos_local)
        elif self.__leg_index == 5:  # -225 or 135 degree:
            self.__mount_position = point3d(-leg_mount_other_x, leg_mount_other_y, 0)
            self.__local_conv = rotate225
            self.__world_conv = rotate135
            self.__tip_pos_local = point3d(p6_x, p6_y, p6_z)
            self.__tip_pos = self.translate2world(self.__tip_pos_local)
        else:
            raise ValueError

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
        """坐标原点在根部舵机安装处"""
        angles = [0.0] * 3

        x = target_point.x - leg_root2joint1
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

    def __move(self, target_point_local: point3d):
        angles = self.__inverse_kinematics(target_point_local)
        # Logging info
        for i in range(3):
            self.__servos[i].set_angle(angles[i])


class VirtualLeg(Leg):
    def __init__(self, leg_index):
        super(VirtualLeg, self).__init__(leg_index)
        self.joint_angles = [0, 30, -15]
        self.leg_vectors_local = self.__forward_kinematics(self.joint_angles)
        self.leg_vectors = [self.translate2world(point) for point in self.leg_vectors_local]

    def __forward_kinematics(self, angles):
        """leg_vectors: point3d list with length of 5"""
        radians = [angle * pi / 180 for angle in angles]
        joint1_pos = point3d(leg_root2joint1, 0, 0)
        joint2_pos = joint1_pos + point3d(leg_joint1_2joint2 * cos(radians[0]), leg_joint1_2joint2 * sin(radians[0]), 0)
        joint3_pos = joint2_pos + point3d(leg_joint2_2joint3 * cos(radians[1]) * cos(radians[0]),
                                          leg_joint2_2joint3 * cos(radians[1]) * sin(radians[0]),
                                          leg_joint2_2joint3 * sin(radians[1]))
        joint4_pos = joint3_pos + point3d(cos(radians[1] + radians[2] - hpi) * leg_joint3_2tip * cos(radians[0]),
                                          cos(radians[1] + radians[2] - hpi) * leg_joint3_2tip * sin(radians[0]),
                                          sin(radians[1] + radians[2] - hpi) * leg_joint3_2tip)

        leg_vectors_local = [point3d(0, 0, 0), joint1_pos, joint2_pos, joint3_pos, joint4_pos]

        return leg_vectors_local

    def __move(self, target_point_local: point3d):
        angles = self.__inverse_kinematics(target_point_local)
        self.joint_angles = angles
        # To simulate movement on matplotlib figure
        self.leg_vectors_local = self.__forward_kinematics(angles)
        self.leg_vectors = [self.translate2world(point) for point in self.leg_vectors_local]

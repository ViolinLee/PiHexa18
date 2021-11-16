# -*- coding: utf-8 -*-

from movement import Movement, MovementMode
from leg import Leg, VirtualLeg
from config import *
from base import point3d
from servo import Servo


class Hexapod(object):
    def __init__(self):
        self.__legs = [Leg(i) for i in range(6)]
        self._movement = Movement(MovementMode.MOVEMENT_STANDBY.value, False)
        self._mode = MovementMode.MOVEMENT_STANDBY.value
        self.servo = None

    def init(self, setting=False):
        self.load_calibration(calibration_path)
        if not setting:
            self.process_movement(MovementMode.MOVEMENT_STANDBY.value)
        print("PiHexa init done.")

    def process_movement(self, mode, elapsed=0):  # 重要函数，与步态执行有关
        if self._mode != mode:
            self._mode = mode
            self._movement.set_mode(self._mode)

        location = self._movement.next(elapsed=elapsed)
        for i in range(6):
            self.__legs[i].move_tip(location.get(i))

    def process_calibration(self):
        return

    def load_calibration(self, json_path):
        return


class VirtualHexapod(Hexapod):
    def __init__(self, ax, origin=(0, 0, 0), initial_height=standby_z):
        super(VirtualHexapod, self).__init__()
        self.__legs = [VirtualLeg(i) for i in range(6)]
        self.ax = ax
        self.initial_height = initial_height
        self.body_vectors = [point3d(origin[0] + leg_mount_other_x, origin[1] + leg_mount_other_y, origin[2]),
                             point3d(origin[0] + leg_mount_left_right_x, origin[1], origin[2]),
                             point3d(origin[0] + leg_mount_other_x, origin[1] - leg_mount_other_y, origin[2]),
                             point3d(origin[0] - leg_mount_other_x, origin[1] - leg_mount_other_y, origin[2]),
                             point3d(origin[0] - leg_mount_left_right_x, origin[1], origin[2]),
                             point3d(origin[0] - leg_mount_other_x, origin[1] + leg_mount_other_y, origin[2]),
                             point3d(origin[0] + leg_mount_other_x, origin[1] + leg_mount_other_y, origin[2])]

    def draw_body(self, color='black'):
        x_data = [point.x for point in self.body_vectors]
        y_data = [point.y for point in self.body_vectors]
        z_data = [point.z for point in self.body_vectors]
        self.ax.plot(x_data, y_data, z_data, color=color)

    def draw_legs(self, color='blue'):
        for i, leg in enumerate(self.__legs):
            x_data = [point.x for point in leg.leg_vectors]
            y_data = [point.y for point in leg.leg_vectors]
            z_data = [point.z for point in leg.leg_vectors]
            self.ax.plot(x_data, y_data, z_data, color=color)

    def process_movement(self, mode, elapsed=0):  # 重要函数，与步态执行有关
        if self._mode != mode:
            self._mode = mode
            print("mode:", mode, "self.mode:", self._mode)
            self._movement.set_mode(self._mode)

        location = self._movement.next(elapsed=elapsed)
        for i in range(6):
            self.__legs[i].move_tip(location.get(i))



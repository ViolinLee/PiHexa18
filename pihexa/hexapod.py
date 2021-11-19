# -*- coding: utf-8 -*-

import json
from movement import Movement, MovementMode
from leg import Leg, VirtualLeg
from config import *
from base import point3d
from servo import Servo
from time import sleep
from datetime import datetime


class Hexapod(object):
    def __init__(self):
        self.leg_servo = Servo()
        self._movement = Movement(MovementMode.MOVEMENT_STANDBY.value, False)
        self._mode = MovementMode.MOVEMENT_STANDBY.value
        self.__legs = [Leg(i, self.leg_servo) for i in range(6)]

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

    def process_calibration(self, calibration_data):
        if calibration_data != self.leg_servo.offset:
            # Update servo offset attribute
            self.leg_servo.set_offset(calibration_data)
            # Set all servos middle angle
            for leg_id in range(6):
                for part_id in range(3):
                    self.leg_servo.set_angle(leg_id, part_id, 90)
            sleep(0.02)
        else:
            pass

    def load_calibration(self, json_path):
        with open(json_path, 'r') as f:
            json_data = json.load(f)
            calibration_data = json_data['calibration']
            version = json_data['update_time']
            self.leg_servo.set_offset(calibration_data)
        print("Load calibration data: {0}\nVersion: {1}".format(calibration_data, version))

    def save_calibration(self, json_path):
        with open(json_path, 'w') as f:
            calibration_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            json_dict = {'update_time': calibration_time,
                         'calibration': self.leg_servo.offset}
            json.dump(json_dict, f, ensure_ascii=False)
        print("Save calibration data: {0}\nTime: {1}".format(self.leg_servo.offset, calibration_time))


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



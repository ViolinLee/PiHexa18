# -*- coding: utf-8 -*-

from base import *
from movement import MovementTable

"""
This file is generated, dont directly modify content...
"""

# 后退
backward_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                  locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
backward_entries = [0, 10]
backward_table = MovementTable(backward_paths, 20, 20, backward_entries, 2)

# 攀登
climb_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
               locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
climb_entries = [0, 10]
climb_table = MovementTable(climb_paths, 20, 30, climb_entries, 2)

# 前进
forward_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                 locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
forward_entries = [0, 10]
forward_table = MovementTable(forward_paths, 20, 20, forward_entries, 2)

# 快速前进
forward_fast_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                      locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
forward_fast_entries = [0, 10]
forward_fast_table = MovementTable(forward_fast_paths, 20, 20, forward_fast_entries, 2)

# 绕 X 轴旋转
rotate_x_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                  locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
rotate_x_entries = [0, 10]
rotate_x_table = MovementTable(rotate_x_paths, 20, 20, rotate_x_entries, 2)

# 绕 Y 轴旋转
rotate_y_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                  locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
rotate_y_entries = [0, 10]
rotate_y_table = MovementTable(rotate_y_paths, 20, 20, rotate_y_entries, 2)

# 绕 Z 轴旋转
rotate_zy_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                   locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
rotate_z_entries = [0, 10]
rotate_z_table = MovementTable(rotate_y_paths, 20, 20, rotate_z_entries, 2)

# 左平移
shift_left_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                    locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
shift_left_entries = [0, 10]
shift_left_table = MovementTable(shift_left_paths, 20, 20, shift_left_entries, 2)

# 右平移
shift_right_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                     locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
shift_right_entries = [0, 10]
shift_right_table = MovementTable(shift_right_paths, 20, 20, shift_right_entries, 2)

# 左转弯
turn_left_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                   locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
turn_left_entries = [0, 10]
turn_left_table = MovementTable(turn_left_paths, 20, 20, turn_left_entries, 2)

# 右转弯
turn_right_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
                    locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
turn_right_entries = [0, 10]
turn_right_table = MovementTable(turn_right_paths, 20, 20, turn_right_entries, 2)

# 扭动
twist_paths = [locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d()),
               locations(point3d(), point3d(), point3d(), point3d(), point3d(), point3d())]
twist_entries = [0, 10]
twist_table = MovementTable(twist_paths, 20, 20, twist_entries, 2)

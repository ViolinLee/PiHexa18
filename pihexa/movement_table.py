# -*- coding: utf-8 -*-

from movement_paths import *
from config import k_standby, standby_entries, standby_entries_count

"""
This file is generated, dont directly modify content...
"""


class MovementTable(object):
    def __init__(self, table, length, step_duration, entries, entries_count):
        self.table = [locations.from_list(path_point) for path_point in table]
        self.length = length
        self.step_duration = step_duration
        self.entries = entries
        self.entries_count = entries_count


standby_table = MovementTable([k_standby], 1, 20, standby_entries, standby_entries_count)
backward_table = MovementTable(backward_paths, backward_length, backward_duration, backward_entries, len(backward_entries))
climb_table = MovementTable(climb_paths, 20, 30, climb_entries, len(climb_entries))
forward_table = MovementTable(forward_paths, 20, 20, forward_entries, len(forward_entries))
forward_fast_table = MovementTable(forward_fast_paths, 20, 20, forward_fast_entries, 2)
rotate_x_table = MovementTable(rotate_x_paths, 20, 20, rotate_x_entries, 2)
rotate_y_table = MovementTable(rotate_y_paths, 20, 20, rotate_y_entries, 2)
rotate_z_table = MovementTable(rotate_z_paths, 20, 20, rotate_z_entries, 2)
shift_left_table = MovementTable(shift_left_paths, 20, 20, shift_left_entries, 2)
shift_right_table = MovementTable(shift_right_paths, 20, 20, shift_right_entries, 2)
turn_left_table = MovementTable(turn_left_paths, 20, 20, turn_left_entries, 2)
turn_right_table = MovementTable(turn_right_paths, 20, 20, turn_right_entries, 2)
twist_table = MovementTable(twist_paths, 20, 20, twist_entries, 2)


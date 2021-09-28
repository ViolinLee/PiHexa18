# -*- coding: utf-8 -*-

from config import *
from math_utils import *
from movement import MovementTable

standby_z = leg_joint3_2tip * COS15 - leg_joint2_2joint3 * SIN30
left_right_x = leg_mount_left_right_x + leg_root2joint1 + leg_joint1_2joint2 + leg_joint2_2joint3 * COS30 + leg_joint3_2tip * SIN15
other_x = leg_mount_other_x + (leg_root2joint1 + leg_joint1_2joint2 + leg_joint2_2joint3 * COS30 + leg_joint3_2tip * SIN15) * COS45
other_y = leg_mount_other_y + (leg_root2joint1 + leg_joint1_2joint2 + leg_joint2_2joint3 * COS30 + leg_joint3_2tip * SIN15) * SIN45

p1_x = other_x
p1_y = other_y
p1_z = -standby_z

p2_x = left_right_x
p2_y = 0
p2_z = -standby_z

p3_x = other_x
p3_y = -other_y
p3_z = -standby_z

p4_x = -other_x
p4_y = -other_y
p4_z = -standby_z

p5_x = -left_right_x
p5_y = 0
p5_z = -standby_z

p6_x = -other_x
p6_y = other_y
p6_z = -standby_z

k_standby = locations(point3d(p1_x, p1_y, p1_z),
                      point3d(p2_x, p2_y, p2_z),
                      point3d(p3_x, p3_y, p3_z),
                      point3d(p4_x, p4_y, p4_z),
                      point3d(p5_x, p5_y, p5_z),
                      point3d(p6_x, p6_y, p6_z),)
standby_entries = 0
entries_count = 1  # Number of elements of variable standby_entries
standby_table = MovementTable(k_standby, 1, 20, standby_entries, entries_count)

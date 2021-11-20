# -*- coding: utf-8 -*-
from math_utils import *


# mounting position
leg_mount_left_right_x = 29.87  # position in x direction of the middle legs
leg_mount_other_x = 22.41  # position in x direction of the fore and hind legs
leg_mount_other_y = 55.41  # position in y direction of the fore and hind legs
mount_position = ((leg_mount_other_x, leg_mount_other_y, 0),
                  (leg_mount_left_right_x, 0, 0),
                  (leg_mount_other_x, -leg_mount_other_y, 0),
                  (-leg_mount_other_x, -leg_mount_other_y, 0),
                  (-leg_mount_left_right_x, 0, 0),
                  (-leg_mount_other_x, leg_mount_other_y, 0))

# link length
leg_root2joint1 = 20.75
leg_joint1_2joint2 = 28.0
leg_joint2_2joint3 = 42.6
leg_joint3_2tip = 89.07

# movement parameters (ms)
movement_interval = 5  # 主程序需要的、考虑舵机响应而加的延迟时间
movement_switch_duration = 150  # 步态路径路径点的间隔（计算上）

# calibration results saved path
calibration_path = "calibration.json"
html_path = 'calibration.html'
with open(html_path) as f:
    html_bytes = f.read().encode()

# default mounting angle
default_angle = (-45, 0, 45, 135, 180, 225)

# angle limitation
angleLimitation = ((-45, 45), (-45, 75), (-60, 60))

# movement constance
standby_z = leg_joint3_2tip * COS15 - leg_joint2_2joint3 * SIN30
left_right_x = leg_mount_left_right_x + leg_root2joint1 + leg_joint1_2joint2 + leg_joint2_2joint3 * COS30 + leg_joint3_2tip * SIN15
other_x = leg_mount_other_x + (
            leg_root2joint1 + leg_joint1_2joint2 + leg_joint2_2joint3 * COS30 + leg_joint3_2tip * SIN15) * COS45
other_y = leg_mount_other_y + (
            leg_root2joint1 + leg_joint1_2joint2 + leg_joint2_2joint3 * COS30 + leg_joint3_2tip * SIN15) * SIN45

# paths way points' locations description
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

# for paths generation
default_position = ((other_x, other_y, -standby_z),
                    (left_right_x, 0, -standby_z),
                    (other_x, -other_y, -standby_z),
                    (-other_x, -other_y, -standby_z),
                    (-left_right_x, 0, -standby_z),
                    (-other_x, other_y, -standby_z))

# for paths locations calculation of real robot
k_standby = [(p1_x, p1_y, p1_z),
             (p2_x, p2_y, p2_z),
             (p3_x, p3_y, p3_z),
             (p4_x, p4_y, p4_z),
             (p5_x, p5_y, p5_z),
             (p6_x, p6_y, p6_z)]
standby_entries = (0, )
standby_entries_count = 1  # Number of elements of variable standby_entries

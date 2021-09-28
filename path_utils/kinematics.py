import math
from pihexa.config import leg_root2joint1, leg_joint1_2joint2, leg_joint2_2joint3, leg_joint3_2tip

pi = math.acos(-1)


def ik(to):
    """坐标原点在根部舵机安装处"""
    angles = []
    x = to[0] - leg_root2joint1
    y = to[1]

    angles.append(math.atan2(y, x) * 180 / pi)

    x = math.sqrt(x*x + y*y) - leg_joint1_2joint2
    y = to[2]
    ar = math.atan2(y, x)
    lr2 = x*x + y*y
    lr = math.sqrt(lr2)
    a1 = math.acos((lr2 + leg_joint2_2joint3**2 - leg_joint3_2tip**2)/(2*leg_joint2_2joint3*lr))
    a2 = math.acos((lr2 - leg_joint2_2joint3**2 + leg_joint3_2tip**2)/(2*leg_joint3_2tip*lr))

    angles.append((ar + a1) * 180 / pi)
    angles.append(90 - ((a1 + a2) * 180 / pi))

    return angles

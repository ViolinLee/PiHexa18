# -*- coding: utf-8 -*-

from base import *

"""数学计算相关宏定义"""

sin45 = 0.7071
cos45 = 0.7071


def rotate0(src):
    dest = point3d(src.x, src.y, src.z)
    return dest


def rotate45(src):
    dest = point3d()
    dest.x = src.x * cos45 - src.y * sin45
    dest.y = src.x * sin45 + src.y * cos45
    dest.z = src.z
    return dest


def rotate135(src):
    dest = point3d()
    dest.x = src.x * -cos45 - src.y * sin45
    dest.y = src.x * sin45 + src.y * -cos45
    dest.z = src.z
    return dest


def rotate180(src):
    dest = point3d()
    dest.x = -src.x
    dest.y = -src.x
    dest.z = src.z
    return dest


def rotate225(src):
    dest = point3d()
    dest.x = src.x * -cos45 - src.y * -sin45
    dest.y = src.x * -sin45 + src.y * -cos45
    dest.z = src.z
    return dest


def rotate315(src):
    dest = point3d()
    dest.x = src.x * cos45 - src.y * -sin45
    dest.y = src.x * -sin45 + src.y * cos45
    dest.z = src.z
    return dest


if __name__ == '__main__':





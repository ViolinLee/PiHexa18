# -*- coding: utf-8 -*-

from base import *

"""数学计算相关宏定义"""

SIN30 = 0.5
COS30 = 0.866
SIN45 = 0.7071
COS45 = 0.7071
SIN15 = 0.2588
COS15 = 0.9659


def rotate0(src: point3d):
    dest = point3d(src.x, src.y, src.z)
    return dest


def rotate45(src: point3d):
    dest = point3d()
    dest.x = src.x * COS45 - src.y * SIN45
    dest.y = src.x * SIN45 + src.y * COS45
    dest.z = src.z
    return dest


def rotate135(src: point3d):
    dest = point3d()
    dest.x = src.x * -COS45 - src.y * SIN45
    dest.y = src.x * SIN45 + src.y * -COS45
    dest.z = src.z
    return dest


def rotate180(src: point3d):
    dest = point3d()
    dest.x = -src.x
    dest.y = -src.y
    dest.z = src.z
    return dest


def rotate225(src: point3d):
    dest = point3d()
    dest.x = src.x * -COS45 - src.y * -SIN45
    dest.y = src.x * -SIN45 + src.y * -COS45
    dest.z = src.z
    return dest


def rotate315(src: point3d):
    dest = point3d()
    dest.x = src.x * COS45 - src.y * -SIN45
    dest.y = src.x * -SIN45 + src.y * COS45
    dest.z = src.z
    return dest


if __name__ == '__main__':
    src = point3d(5, 5, 0)
    dest = rotate45(src)
    print(dest.x, dest.y, dest.z)

from collections import deque
import math
import numpy as np

pi = math.pi

# 步态是简单的半圆弧曲线
def semicircle_generator(radius, steps, reverse=False):
    assert (steps % 4) == 0  # steps是啥？把一个圆分成多少步
    half_steps = int(steps/2)

    step_angle = pi / half_steps
    step_stride = 2*radius / half_steps

    result = []

    # 前半部分，后移（只有y轴改变——腿接触地面）
    for i in range(half_steps):
        result.append((0, radius - i*step_stride, 0))  # 直线 [radius, 0]

    # 第二（后半）部分，以半圆形状前移（y，z 改变）
    for i in range(half_steps):
        angle = pi - step_angle*i  # 范围：[pi, 0]
        y = radius * math.cos(angle)  # pi的范围决定y从负数开始 [-radius, radius]
        z = radius * math.sin(angle)  # y和z组合的半圆
        result.append((0, y, z))  # x一直保持为0？x和y后面都要偏易，z不用

    result = deque(result)
    result.rotate(int(steps/4))  # y从3/4处开始轮转，而不是0处

    if reverse:
        result = deque(reversed(result))
        result.rotate(1)

    return result


def semicircle2_generator(steps, y_radius, z_radius, x_radius, reverse=False):
    assert (steps % 4) == 0
    half_steps = int(steps / 2)

    step_angle = pi / half_steps
    step_y_stride = 2 * y_radius / half_steps


    result = []

    # 前半部分，后移（只有y轴改变——腿接触地面）
    for i in range(half_steps):
        result.append((0, y_radius - i * step_y_stride, 0))  # 直线 [radius, 0]

    # 第二（后半）部分，以半圆形状前移（y，z 改变）
    for i in range(half_steps):
        angle = pi - step_angle * i
        y = y_radius * math.cos(angle)
        z = z_radius * math.sin(angle)
        x = x_radius * math.sin(angle)  # x的意义是啥？
        result.append((x, y, z))

    result = deque(result)
    result.rotate(int(steps / 4))

    if reverse:
        result = deque(reversed(result))
        result.rotate(1)

    return result


def get_rotate_x_matrix(angle):
    angle = angle * pi / 180
    return np.array([[1, 0, 0, 0],
                     [0, math.cos(angle), -math.sin(angle), 0],
                     [0, math.sin(angle), math.cos(angle), 0],
                     [0, 0, 0, 1]])


def get_rotate_y_matrix(angle):
    angle = angle * pi / 180
    return np.array([[math.cos(angle), 0, math.sin(angle), 0],
                     [0, 1, 0, 0],
                     [-math.sin(angle), 0, math.cos(angle), 0],
                     [0, 0, 0, 1]])


def get_rotate_z_matrix(angle):
    angle = angle * pi / 180
    return np.array([[math.cos(angle), -math.sin(angle), 0, 0],
                     [math.sin(angle), math.cos(angle), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def matrix_mul(tr_matrix, pt):
    ptx = list(pt) + [1]
    return list(np.matmul(tr_matrix, np.array(ptx).T))[:-1]


def point_rotate_x(pt, angle):
    tr_matrix = get_rotate_x_matrix(angle)
    return matrix_mul(tr_matrix, pt)


def point_rotate_y(pt, angle):
    tr_matrix = get_rotate_y_matrix(angle)
    return matrix_mul(tr_matrix, pt)


def point_rotate_z(pt, angle):
    tr_matrix = get_rotate_z_matrix(angle)
    return matrix_mul(tr_matrix, pt)


def path_rotate_x(path, angle):
    return [point_rotate_x(p, angle) for p in path]


def path_rotate_y(path, angle):
    return [point_rotate_y(p, angle) for p in path]


def path_rotate_z(path, angle):
    return [point_rotate_z(p, angle) for p in path]


if __name__ == "__main__":
    m = get_rotate_z_matrix(45)
    pt = [0, 1, 0]
    print(matrix_mul(m, pt))

    rotate_angle = 45
    print(point_rotate_z(pt, rotate_angle))

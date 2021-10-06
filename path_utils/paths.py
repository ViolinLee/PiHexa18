from collections import deque

from lib import semicircle_generator, semicircle2_generator
from lib import path_rotate_z
from lib import get_rotate_x_matrix, get_rotate_y_matrix, get_rotate_z_matrix
from math import pi, cos, sin, atan2


def forward_path_gen():
    g_steps = 20
    g_radius = 25
    step_duration = 20
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    path = semicircle_generator(g_radius, g_steps)

    mir_path = deque(path)
    mir_path.rotate(half_steps)  # 相对的腿错开半个g_steps的运动规律

    return [path, mir_path, path, mir_path, path, mir_path], mode, step_duration, (0, half_steps)


def forward_fast_path_gen():
    g_steps = 20
    y_radius = 50  # 在保持步数不变的同时，延长y方向的跨度
    z_radius = 30
    x_radius = 10
    step_duration = 20
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    right_path = semicircle2_generator(g_steps, y_radius, z_radius, x_radius)
    left_path = semicircle2_generator(g_steps, y_radius, z_radius, -x_radius)

    mir_right_path = deque(right_path)
    mir_right_path.rotate(half_steps)

    mir_left_path = deque(left_path)
    mir_left_path.rotate(half_steps)

    return [right_path, mir_right_path, right_path, mir_left_path, left_path, mir_left_path], mode, step_duration, (0, half_steps)


def backward_path_gen():
    g_steps = 20
    g_radius = 25
    step_duration = 20
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    path = semicircle_generator(g_radius, g_steps, reverse=True)

    mir_path = deque(path)
    mir_path.rotate(half_steps)

    return [path, mir_path, path, mir_path, path, mir_path], mode, step_duration, (0, half_steps)


def turn_left_path_gen():
    g_steps = 20
    g_radius = 25
    step_duration = 20
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps/2)

    path = semicircle_generator(g_radius, g_steps)

    mir_path = deque(path)
    mir_path.rotate(half_steps)

    return [path_rotate_z(path, 45),
            path_rotate_z(mir_path, 0),
            path_rotate_z(path, 315),
            path_rotate_z(mir_path, 255),
            path_rotate_z(path, 180),
            path_rotate_z(mir_path, 135)], mode, step_duration, (0, half_steps)


def turn_right_path_gen():
    g_steps = 20
    g_radius = 25
    step_duration = 20
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    path = semicircle_generator(g_radius, g_steps)

    mir_path = deque(path)
    mir_path.rotate(half_steps)

    return [path_rotate_z(path, 45+180),
            path_rotate_z(mir_path, 0+180),
            path_rotate_z(path, 315+180),
            path_rotate_z(mir_path, 225+180),
            path_rotate_z(path, 180+180),
            path_rotate_z(mir_path, 135+180)], mode, step_duration, (0, half_steps)


def shift_left_path_gen():
    g_steps = 20
    g_radius = 25
    step_duration = 20
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    path = semicircle_generator(g_radius, g_steps)
    path = path_rotate_z(path, 90)  # 路径方向旋转90度即平移

    mir_path = deque(path)
    mir_path.rotate(half_steps)

    return [path, mir_path, path, mir_path, path, mir_path], mode, step_duration, (0, half_steps)


def shift_right_path_gen():
    g_steps = 20
    g_radius = 25
    step_duration = 20
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    path = semicircle_generator(g_radius, g_steps)
    path = path_rotate_z(path, 270)  # 路径方向旋转270度即平移

    mir_path = deque(path)
    mir_path.rotate(half_steps)

    return [path, mir_path, path, mir_path, path, mir_path], mode, step_duration, (0, half_steps)


def climb_path_gen():
    g_steps = 20
    y_radius = 20
    z_radius = 80
    x_radius = 30
    z_shift = -30
    step_duration = 30
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    right_path = [(x, y, z + z_shift) for x, y, z in semicircle2_generator(g_steps, y_radius, z_radius, x_radius)]
    left_path = [(x, y, z + z_shift) for x, y, z in semicircle2_generator(g_steps, y_radius, z_radius, -x_radius)]

    mir_right_path = deque(right_path)
    mir_right_path.rotate(half_steps)

    mir_left_path = deque(left_path)
    mir_left_path.rotate(half_steps)

    return [right_path, mir_right_path, right_path, mir_left_path, left_path, mir_left_path], mode, step_duration, (0, half_steps)


def rotate_x_path_gen():  # 绕x轴旋转，保证旋转矩阵索引为0的collum为[1, 0, 0, 0]
    g_steps = 20
    swing_angle = 15
    x_radius = 15
    step_duration = 50
    mode = "matrix"

    assert (g_steps % 4) == 0
    quarter = int(g_steps / 4)

    result = []
    step_angle = swing_angle / quarter
    step_offset = x_radius / quarter

    for i in range(quarter):
        m = get_rotate_x_matrix(swing_angle - i * step_angle)  # [swing_angle, 0]
        m[1, 3] = -i * step_offset  # [0, -x_radius] 这个有什么意义？
        result.append(m)

    for i in range(quarter):
        m = get_rotate_x_matrix(-i * step_angle)  # [0, -swing_angle]
        m[1, 3] = -x_radius + i * step_offset  # [-x_radius, 0]
        result.append(m)

    for i in range(quarter):
        m = get_rotate_x_matrix(i * step_angle - swing_angle)  # [-swing_angle, 0]
        m[1, 3] = i * step_offset  # [0, x_radius]
        result.append(m)

    for i in range(quarter):
        m = get_rotate_x_matrix(i * step_angle)    # [0, swing_angle]
        m[1, 3] = x_radius - i * step_offset  # [x_radius, 0]
        result.append(m)

    return result, mode, step_duration, (0, quarter*2)


def rotate_y_path_gen():
    g_steps = 20
    swing_angle = 15
    y_radius = 15
    step_duration = 50
    mode = "matrix"

    assert (g_steps % 4) == 0
    quarter = int(g_steps / 4)

    result = []
    step_angle = swing_angle / quarter
    step_offset = y_radius / quarter

    for i in range(quarter):
        m = get_rotate_y_matrix(swing_angle - i * step_angle)  # [swing_angle, 0]
        m[0, 3] = -i * step_offset
        result.append(m)

    for i in range(quarter):
        m = get_rotate_y_matrix(-i * step_angle)  # [0, -swing_angle]
        m[0, 3] = -y_radius + i * step_offset
        result.append(m)

    for i in range(quarter):
        m = get_rotate_y_matrix(i * step_angle - swing_angle)  # [-swing_angle, 0]
        m[0, 3] = i * step_offset
        result.append(m)

    for i in range(quarter):
        m = get_rotate_y_matrix(i * step_angle)    # [0, swing_angle]
        m[0, 3] = y_radius - i * step_offset
        result.append(m)

    return result, mode, step_duration, (0, quarter*2)


def rotate_z_path_gen():
    """
    g_steps = 20
    swing_angle = 15
    z_radius = 15
    step_duration = 50
    mode = "matrix"

    assert (g_steps % 4) == 0
    quarter = int(g_steps / 4)

    result = []
    step_angle = swing_angle / quarter
    step_offset = z_radius / quarter

    for i in range(quarter):
        m = get_rotate_z_matrix(swing_angle - i * step_angle)  # [swing_angle, 0]
        #m[0, 3] = -i * step_offset
        result.append(m)

    for i in range(quarter):
        m = get_rotate_z_matrix(-i * step_angle)  # [0, -swing_angle]
        #m[0, 3] = -z_radius + i * step_offset
        result.append(m)

    for i in range(quarter):
        m = get_rotate_z_matrix(i * step_angle - swing_angle)  # [-swing_angle, 0]
        #m[0, 3] = i * step_offset
        result.append(m)

    for i in range(quarter):
        m = get_rotate_z_matrix(i * step_angle)  # [0, swing_angle]
        #m[0, 3] = z_radius - i * step_offset
        result.append(m)

    return result, mode, step_duration, (0, quarter * 2)
    """

    g_steps = 20
    z_lift = 4.5
    xy_radius = 1
    step_duration = 50
    mode = "matrix"

    result = []
    step_angle = 2 * pi / g_steps
    for i in range(g_steps):
        x = xy_radius * cos(i*step_angle)  # [1, 0, -1, 0, 1]
        y = xy_radius * sin(i*step_angle)  # [0, 1, 0, -1, 0]

        m = get_rotate_y_matrix(atan2(x, z_lift) * 180 / pi) @ get_rotate_x_matrix(atan2(y, z_lift) * 180 / pi)
        result.append(m)

    return result, mode, step_duration, range(g_steps)




def twist_path_gen():
    g_steps = 20
    raise_angle = 3
    twist_x_angle = 20
    twist_y_angle = 12
    step_duration = 50
    mode = "matrix"

    assert (g_steps % 4) == 0

    quarter = int(g_steps / 4)
    step_x_angle = twist_x_angle / quarter
    step_y_angle = twist_y_angle / quarter
    m = get_rotate_x_matrix(raise_angle)

    result = []
    for i in range(quarter):
        result.append(m @ get_rotate_z_matrix(i*step_x_angle) @ get_rotate_x_matrix(i*step_y_angle))

    for i in range(quarter):
        result.append(m @ get_rotate_z_matrix((quarter-i)*step_x_angle) @ get_rotate_x_matrix((quarter-i)*step_y_angle))

    for i in range(quarter):
        result.append(m @ get_rotate_z_matrix(-i*step_x_angle) @ get_rotate_x_matrix(i*step_y_angle))

    for i in range(quarter):
        result.append(m @ get_rotate_z_matrix((-quarter+i)*step_x_angle) @ get_rotate_x_matrix((quarter-i)*step_y_angle))

    return result, mode, step_duration, [0, quarter*2]


paths_generators = {'forward': forward_path_gen,
                    'forward_fast': forward_fast_path_gen,
                    'backward': backward_path_gen,
                    'turn_left': turn_left_path_gen,
                    'turn_right': turn_right_path_gen,
                    'shift_left': shift_left_path_gen,
                    'shift_right': shift_right_path_gen,
                    'climb': climb_path_gen,
                    'rotate_x': rotate_x_path_gen,
                    'rotate_y': rotate_y_path_gen,
                    'rotate_z': rotate_z_path_gen,
                    'twist': twist_path_gen}


if __name__ == "__main__":
    result, mode, duration, _ = rotate_y_path_gen()
    resultx, modex, durationx, _ = rotate_x_path_gen()

    for i, res in enumerate(result):
        print(result[i], '\n', resultx[i])
        print("\n")



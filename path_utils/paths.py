from collections import deque

from lib import semicircle_generator, semicircle2_generator


def forward_path_gen():
    g_steps = 20
    g_radius = 25
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    path = semicircle_generator(g_radius, g_steps)

    mir_path = deque(path)
    mir_path.rotate(half_steps)

    return [path, mir_path, path, mir_path, path, mir_path], mode, g_steps, (0, half_steps)


def forward_fast_path_gen():
    g_steps = 20
    y_radius = 50  # 在保持步数不变的同时，延长y方向的跨度
    z_radius = 30
    x_radius = 10
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    right_path = semicircle2_generator(g_steps, y_radius, z_radius, x_radius)
    left_path = semicircle2_generator(g_steps, y_radius, z_radius, -x_radius)

    mir_right_path = deque(right_path)
    mir_right_path.rotate(half_steps)

    mir_left_path = deque(left_path)
    mir_left_path.rotate(half_steps)

    return [right_path, mir_right_path, right_path, mir_left_path, left_path, mir_left_path], mode, g_steps, (0, half_steps)


def backward_path_gen():
    g_steps = 20
    g_radius = 25
    mode = "shift"

    assert (g_steps % 4) == 0
    half_steps = int(g_steps / 2)

    path = semicircle_generator(g_radius, g_steps, reverse=True)

    mir_path = deque(path)
    mir_path.rotate(half_steps)

    return [path, mir_path, path, mir_path, path, mir_path], mode, g_steps, (0, half_steps)



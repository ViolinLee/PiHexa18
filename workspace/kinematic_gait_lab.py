import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import pi, cos, sin
from kinematics import ik
from pihexa.base import point3d


# Configuration
WINDOW_SIZE = 400
ANIMATE_INTERVAL = 50

# Setting up 3D figure
fig = plt.figure()
ax = Axes3D(fig)
color = 'blue'

# gait constants
home_x = [87.68,   0.0, -87.68,  -87.68,    0.0,  87.68]  # coxa-to-toe home positions
home_y = [87.68, 124.0,  87.68,  -87.68, -124.0, -87.68]
home_z = [-85.0,  -85.0,  -85.0,   -85.0,  -85.0,  -85.0]
amplitudeX, amplitudeY, amplitudeZ = 15, 10, 20

# movement configuration
frame_time_ms = 20


def left_rotate_path(path: list, rotation_num):
    # method 1
    rotated_path = path[rotation_num:] + path[:rotation_num]
    return rotated_path


def trot_path_global(gait_speed=0):
    # amplitudeX, amplitudeY, amplitudeZ = compute_amplitude()
    duration = 1080 if gait_speed == 0 else 3240
    num_ticks = int(duration / frame_time_ms / 2)  # total ticks divided into 2 stages, 'num_ticks' = ticks per stages
    fr_path = [point3d()] * num_ticks

    for stage_id in range(2):  # A cycle is divided into 2 stages
        for tick_cnt in range(num_ticks):
            interp_id = stage_id*num_ticks + tick_cnt
            if stage_id == 0:
                fr_path[interp_id].x = home_x[0] - amplitudeX * cos(pi * tick_cnt / num_ticks)
                fr_path[interp_id].y = home_y[0] - amplitudeY * cos(pi * tick_cnt / num_ticks)
                fr_path[interp_id].z = home_z[0] + abs(amplitudeZ) * sin(pi * tick_cnt / num_ticks)
            else:
                fr_path[interp_id].x = home_x[0] + amplitudeX * cos(pi * tick_cnt / num_ticks)
                fr_path[interp_id].y = home_y[0] + amplitudeY * cos(pi * tick_cnt / num_ticks)
                fr_path[interp_id].z = home_z[0]

    fl_path = left_rotate_path(fr_path, num_ticks)
    br_path = fr_path
    bl_path = fr_path

    return fr_path, br_path, fl_path, bl_path


def creep_path_global(gait_speed=0):
    # amplitudeX, amplitudeY, amplitudeZ = compute_amplitude()
    duration = 1080 if gait_speed == 0 else 3240
    num_ticks = int(duration / frame_time_ms / 6)  # total ticks divided into 6 stages, 'num_ticks' = ticks per stages
    fr_path, bl_path = [point3d()] * num_ticks, [point3d()] * num_ticks

    for stage_id in range(6):  # A cycle is divided into 2 stages
        for tick_cnt in range(num_ticks):
            interp_id = stage_id * num_ticks + tick_cnt
            if stage_id == 0:
                fr_path[interp_id].x = home_x[0] - amplitudeX * cos(pi * tick_cnt / num_ticks)
                fr_path[interp_id].y = home_y[0] - amplitudeY * cos(pi * tick_cnt / num_ticks)
                fr_path[interp_id].z = home_z[0] + abs(amplitudeZ) * sin(pi * tick_cnt / num_ticks)

                bl_path[interp_id].x = home_x[2]
                bl_path[interp_id].y = home_y[2]
                bl_path[interp_id].z = home_z[2]
            elif stage_id == 1:
                fr_path[interp_id].x = home_x[0] + amplitudeX * cos(pi/2 * tick_cnt / num_ticks)
                fr_path[interp_id].y = home_y[0] + amplitudeY * cos(pi/2 * tick_cnt / num_ticks)
                fr_path[interp_id].z = home_z[0]

                bl_path[interp_id].x = home_x[2] - amplitudeX * sin(pi/2 * tick_cnt / num_ticks)
                bl_path[interp_id].y = home_y[2] - amplitudeY * sin(pi/2 * tick_cnt / num_ticks)
                bl_path[interp_id].z = home_z[2]
            elif stage_id == 2:
                fr_path[interp_id].x = home_x[0]
                fr_path[interp_id].y = home_y[0]
                fr_path[interp_id].z = home_z[0]

                bl_path[interp_id].x = home_x[0]
                bl_path[interp_id].y = home_y[0]
                bl_path[interp_id].z = home_z[0]
            elif stage_id == 3:
                fr_path[interp_id].x = home_x[0]
                fr_path[interp_id].y = home_y[0]
                fr_path[interp_id].z = home_z[0]

                bl_path[interp_id].x = home_x[0]
                bl_path[interp_id].y = home_y[0]
                bl_path[interp_id].z = home_z[0]
            elif stage_id == 4:
                fr_path[interp_id].x = home_x[0]
                fr_path[interp_id].y = home_y[0]
                fr_path[interp_id].z = home_z[0]

                bl_path[interp_id].x = home_x[0]
                bl_path[interp_id].y = home_y[0]
                bl_path[interp_id].z = home_z[0]
            elif stage_id == 5:
                fr_path[interp_id].x = home_x[0]
                fr_path[interp_id].y = home_y[0]
                fr_path[interp_id].z = home_z[0]

                bl_path[interp_id].x = home_x[0]
                bl_path[interp_id].y = home_y[0]
                bl_path[interp_id].z = home_z[0]

    fl_path = left_rotate_path(fr_path, num_ticks)
    br_path = fr_path
    bl_path = fr_path

    return fr_path, br_path, fl_path, bl_path


def animate_fr_leg(i):
    x_data, y_data, y_data = []
    ax.plot(x_data, y_data, y_data, color=color)


if __name__ == '__main__':
    ani = animation.FuncAnimation(fig, animate_fr_leg, interval=ANIMATE_INTERVAL)
    plt.show()



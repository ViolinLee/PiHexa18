import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pynput import keyboard
from hexapod import VirtualHexapod

# Initialize: 0-normal mode   1-setting mode (for servo calibration)
setup_mode = 0

# Configuration
WINDOW_SIZE = 400
ANIMATE_INTERVAL = 50

# Setting up 3D matplotlib figure
fig = plt.figure()
ax = Axes3D(fig)

# Global variable
mode = 0  # action mode
x = y = z = roll = pitch = yaw = 0

# Hexapod instance
pihexa = VirtualHexapod(ax=ax)
# pihexa.init(setting=(setup_mode == 1))


def on_press_callback(key):
    global mode, x, y, z, roll, pitch, yaw

    if key == keyboard.Key.esc:
        return False
    try:
        k = key.char
    except:
        k = key.name
    print(type(k), k)

    if k in ['z']:
        mode = 10
    elif k in ['x']:
        mode = 11
    elif k in ['c']:
        mode = 12
    else:
        try:
            mode = int(k)
        except:
            pass

    return


def setup():
    ax.clear()

    ax.set_aspect("equal")
    ax.set_xlim3d(-WINDOW_SIZE / 2, WINDOW_SIZE / 2)
    ax.set_ylim3d(-WINDOW_SIZE / 2, WINDOW_SIZE / 2)
    ax.set_zlim3d(-pihexa.initial_height, WINDOW_SIZE - pihexa.initial_height)

    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_zlabel('z (mm)')


def animate(i):
    global mode
    setup()

    pihexa.process_movement(mode)
    pihexa.draw_body()
    pihexa.draw_legs()


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press_callback)
    listener.start()

    ani = animation.FuncAnimation(fig, animate, interval=ANIMATE_INTERVAL)
    plt.show()

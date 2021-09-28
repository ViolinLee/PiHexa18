import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pynput import keyboard
from virtual_pihexa import VirtualPiHexa

# Configuration
WINDOW_SIZE = 150
ANIMATE_INTERVAL = 50

# Setting up 3D matplotlib figure
fig = plt.figure()
ax = Axes3D(fig)

pihexa = VirtualPiHexa(ax=ax)


def on_press_callback(key):
    global x, y, z, roll, pitch, yaw

    if key == keyboard.Key.esc:
        return False
    try:
        k = key.char
    except:
        key = key.name

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
    global x, y, z, roll, pitch, yaw
    setup()

    pihexa.draw_body()
    pihexa.draw_legs()


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press_callback)
    listener.start()

    ani = animation.FuncAnimation(fig, animate, interval=ANIMATE_INTERVAL)
    plt.show()

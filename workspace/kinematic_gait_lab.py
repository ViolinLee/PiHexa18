import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from kinematics import ik


# Configuration
WINDOW_SIZE = 400
ANIMATE_INTERVAL = 50

# Setting up 3D figure
fig = plt.figure()
ax = Axes3D(fig)
color = 'blue'


def trot_gait():
    return


def creep_gait():
    return


def animate_fr_leg(i):
    x_data, y_data, y_data = []
    ax.plot(x_data, y_data, y_data, color=color)


if __name__ == '__main__':
    ani = animation.FuncAnimation(fig, animate_fr_leg, interval=ANIMATE_INTERVAL)
    plt.show()



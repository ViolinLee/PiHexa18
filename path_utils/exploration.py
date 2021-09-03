import matplotlib.pyplot as plt
from math import pi, cos, sin, atan2

g_steps = 20
z_lift = 4.5
xy_radius = 1
step_duration = 50
mode = "matrix"

xx = []
yy = []
atxx = []
atyy = []
step_angle = 2 * pi / g_steps
for i in range(g_steps):
    x = xy_radius * cos(i * step_angle)  # [1, 0, -1, 0, 1]
    y = xy_radius * sin(i * step_angle)  # [0, 1, 0, -1, 0]
    xx.append(x)
    yy.append(y)

    atx = atan2(x, z_lift) * 180 / pi
    aty = atan2(y, z_lift) * 180 / pi
    atxx.append(atx)
    atyy.append(aty)

    # m = get_rotate_y_matrix(atan2(x, z_lift) * 180 / pi) * get_rotate_x_matrix(atan2(y, z_lift) * 180 / pi)


plt.figure()
#plt.plot(xx, yy)

plt.plot(range(len(atxx)), atxx)
plt.show()

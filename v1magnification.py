import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy import optimize


# Define a function to convert polar coordinates to Euclidean coordinates
def polar_to_euclidean(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

# Create an array of angles from 0 to 90 degrees
dtheta = math.pi/180.0
angles = np.arange(0.0, math.pi/2.0, dtheta)

# Create lists to store the x and y coordinates of the points on the unit circle
circle_x = np.array([np.cos(theta) for theta in angles])
circle_y = np.array([np.sin(theta) for theta in angles])

# List of specific angles to plot points at
dot_ids = [0, 1, 2, 5, 10, 20, 40, 60, 80, 89]
colors = ["black", "red", "blue", "magenta", "cyan", "red", "blue", "magenta", "cyan", "black"]



def calc_m(w):
    # return 716.197 / (71.6197 + w) # radians version from Brad
    # return 10 / (0.8 + w)  # degrees version from Brad
    return 525.6 / (1.0 + 33.48*w)  # 1984 radians version

# Define an undefined custom function to convert polar coordinates to Euclidean coordinates
def calc_r(w, m):
    return m * np.sin(w)
    # might need to ensure these are zero when w is zero

def calc_delta_z(m, r):
    dr_dw = np.diff(r)/dtheta  # w is theta; dw is dtheta
    dr_dw = np.append(dr_dw, dr_dw[-1]) # diff loses one element, duplicate last derivative to preserve length
    m_sqr = np.square(m)
    dr_dw_sqr = np.square(dr_dw)
    sqr_dif = np.subtract(m_sqr, dr_dw_sqr)
    return np.sqrt(sqr_dif)

# Define an undefined custom function to convert polar coordinates to Euclidean coordinates
def calc_z(delta_z):
    return np.cumsum(delta_z)*dtheta

m = calc_m(angles)
r = calc_r(angles, m)
delta_z = calc_delta_z(m, r)
z = calc_z(delta_z)


# Circle
plt.figure(figsize=(9, 9))
plt.subplot(321)
plt.plot(circle_x, circle_y)
plt.scatter(circle_x[dot_ids], circle_y[dot_ids], c=colors, marker='o', label='Specific Points')
plt.title('Eye space (unit hemisphere)')
plt.xlabel('axial distance (x)')
plt.ylabel('lateral distance (y)')
plt.xlim(max(circle_x), min(circle_x))
plt.axis('equal')
plt.grid()


# V1
plt.subplot(322)
plt.plot(z, r)
plt.scatter(z[dot_ids], r[dot_ids], c=colors, marker='o', label='Specific Points')
plt.title('V1 cortical space')
plt.xlabel('v1 axial distance (z) (mm)')
plt.ylabel('v1 lateral distance (r) (mm)')
plt.axis('equal')
plt.grid()

# m
plt.subplot(323)
plt.plot(angles, m)
plt.scatter(angles[dot_ids], m[dot_ids], c=colors, marker='o', label='Specific Points')
plt.title('Magnification factor vs angle (debug view)')
plt.xlabel('angle (w) (radians)')
plt.ylabel('magnification factor (m)')
#plt.axis('equal')
plt.grid()

# r
plt.subplot(324)
plt.plot(angles, r)
plt.scatter(angles[dot_ids], r[dot_ids], c=colors, marker='o', label='Specific Points')
plt.title('v1 lateral distance vs angle (debug view)')
plt.xlabel('angle (w) (radians)')
plt.ylabel('v1 lateral distance (r)')
#plt.axis('equal')
plt.grid()

# dz/dw
plt.subplot(325)
plt.plot(angles, delta_z)
plt.scatter(angles[dot_ids], delta_z[dot_ids], c=colors, marker='o', label='Specific Points')
plt.title('v1 axial rate of change w.r.t. Angle (debug view)')
plt.xlabel('angle (w) (radians)')
plt.ylabel('v1 axial rate (dz/dw)')
#plt.axis('equal')
plt.grid()

# z
plt.subplot(326)
plt.plot(angles, z)
plt.scatter(angles[dot_ids], z[dot_ids], c=colors, marker='o', label='Specific Points')
plt.title('v1 depth vs angle (debug view)')
plt.xlabel('angle (w) (radians)')
plt.ylabel('v1 axial distance (z)')
#plt.axis('equal')
plt.grid()

plt.tight_layout()
plt.show()

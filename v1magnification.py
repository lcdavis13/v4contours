import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy import optimize
#from '.utils.calculus' import IncrementalIntegral, local_derivative

def local_derivative_nonnegative(f, x, h=1e-5):
    """
    Derivative of a function that can only be evaluated for x >= 0
    f: The function for which the derivative is to be approximated.
    x: The point or list of points at which the derivative is to be approximated.
    h: The step size for the finite difference. Default is 1e-5.
    """
    x1 = x + h
    x0 = np.where(x - h < 0, 0, x - h)
    dx = x1 - x0
    
    fx1 = f(x1)
    fx0 = f(x0)

    df_dx = (fx1 - fx0) / dx
    return df_dx

class IncrementalIntegral:
    def __init__(self, func, initial_x):
        self.func = func
        self.integrals = []
        self.x_values = sorted(initial_x)

        # Compute initial integrals for the provided x values
        for i in range(len(self.x_values) - 1):
            a, b = self.x_values[i], self.x_values[i + 1]
            result = self._compute_integral(a, b)
            self.integrals.append((b, result))

    def integrate(self, x):
        if not self.integrals or x > self.x_values[-1]:
            # If the list is empty or x is greater than the largest x in the initial list,
            # compute the integral for the new portion
            prev_x = self.x_values[-1] if self.x_values else 0
            result = self._compute_integral(prev_x, x)
            self.integrals.append((x, result))
        else:
            # Find the largest pre-existing x smaller than or equal to the current x
            prev_x, prev_result = max(((xi, yi) for xi, yi in self.integrals if xi <= x), default=(0, 0))

            # Compute the integral only for the new portion
            result = prev_result + self._compute_integral(prev_x, x - prev_x)
            self.integrals.append((x, result))

        return result

    def _compute_integral(self, a, b):
        # Basic numerical integration using the trapezoidal rule for a single trapezoid
        result = 0.5 * (b - a) * (self.func(a) + self.func(b))
        return result
    

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
    return 525.6 / (1.0 + 33.48*np.abs(w))  # 1984 radians version

# Define an undefined custom function to convert polar coordinates to Euclidean coordinates
def calc_r(w, m):
    return m * np.sin(w)


def calc_delta_z(w, m):
    dr_dw = local_derivative_nonnegative(lambda w_: calc_r(w_, calc_m(w_)), w)  # w is theta; dw is dtheta
    m_sqr = np.square(m)
    dr_dw_sqr = np.square(dr_dw)
    sqr_dif = np.maximum(np.subtract(m_sqr, dr_dw_sqr), 0.0)
    return np.sqrt(sqr_dif)

# # Define an undefined custom function to convert polar coordinates to Euclidean coordinates
# def calc_z(delta_z):
#     return np.cumsum(delta_z)*dtheta
#
# m = calc_m(angles)
# r = calc_r(angles, m)
# delta_z = calc_delta_z(m, r)
# z = calc_z(delta_z)

# Create an instance of IncrementalIntegral for the angles
integral_calculator_angles = IncrementalIntegral(
    lambda w: calc_delta_z(w, calc_m(w)), angles)

m = calc_m(angles)
r = calc_r(angles, m)
delta_z = calc_delta_z(m, r)

# Use the IncrementalIntegral to calculate the integral of delta_z with respect to angles
z = np.array([integral_calculator_angles.integrate(angle) for angle in angles])

print(z)


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

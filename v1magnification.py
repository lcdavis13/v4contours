import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy import optimize


# Define a function to convert polar coordinates to Euclidean coordinates
def polar_to_euclidean(r, theta):
    x = r * np.cos(np.radians(theta))
    y = r * np.sin(np.radians(theta))
    return x, y

# Create an array of angles from 0 to 90 degrees
angles = np.arange(0, 91, 1)

# Create lists to store the x and y coordinates of the points on the unit circle
x_coordinates = [np.cos(np.radians(theta)) for theta in angles]
y_coordinates = [np.sin(np.radians(theta)) for theta in angles]

# List of specific angles to plot points at
specific_angles = [0, 1, 2, 3, 4, 5, 10, 20, 40, 60, 80]

# Calculate the coordinates for these specific angles on both curves
specific_coordinates = [polar_to_euclidean(1, theta) for theta in specific_angles]

# Extract x and y coordinates for the specific points
x_specific, y_specific = zip(*specific_coordinates)

# Plot the unit circle using polar coordinates
plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.plot(x_coordinates, y_coordinates)
plt.scatter(x_specific, y_specific, marker='o', label='Specific Points')
plt.title('Unit Circle (Polar Coordinates)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()

def approximate_derivative(f, z, h=1e-5):
    """
    Approximate the derivative of the function f(x) at the point z using the central difference method.
    :param f: The function to be differentiated.
    :param z: The point at which to approximate the derivative.
    :param h: The step size (small positive value).
    :return: The approximate derivative f'(z).
    """
    derivative = (f(z + h) - f(z - h)) / (2 * h)
    return derivative

# Define an undefined custom function to convert polar coordinates to Euclidean coordinates
def Convert(w_deg):
    w_rad = math.radians(w_deg)
    
    # def M_deg(w):
    #     return 716.197 / (71.6197 + w)
    # r_deg = M_deg(w_deg)*np.sin(w_rad)
    
    
    def M_rad(w):
        return 10 / (0.8 + w)
    def R_rad(w):
        return M_rad(w)*np.sin(w)
    r = R_rad(w_rad)
    
    def zprime(w, Rfunc):
        if w == 0.0:
            return 0.0 # to address rounding errors that lead to a negative number under the square root
        m = M_rad(w)
        dr_dw = approximate_derivative(Rfunc, w)
        sqdif = (m ** 2) - (dr_dw ** 2)
        return math.sqrt(sqdif)
    
    # Deg and rad versions of M equations (given to me by Dr. Motter) are surprisingly a bit different curves
    if w_rad == 0.0:
        z = 0.0
    else:
        intres = integrate.quad(lambda w: zprime(w, R_rad), 0, w_rad)
        z, _ = intres
    
    #x = np.cos(np.radians(w))
    #y = np.sin(np.radians(w))
    return z, r


# Define an undefined custom function to convert polar coordinates to Euclidean coordinates
def ConvertDebug(w_deg):
    w_rad = math.radians(w_deg)
    
    # def M_deg(w):
    #     return 716.197 / (71.6197 + w)
    # r_deg = M_deg(w_deg)*np.sin(w_rad)
    
    def M_rad(w):
        return 10 / (0.8 + w)
    
    def R_rad(w):
        return M_rad(w) * np.sin(w)
    
    r = R_rad(w_rad)

    # x = np.cos(np.radians(w))
    # y = np.sin(np.radians(w))
    return w_rad, r

# Create lists to store the x and y coordinates of the points on the unit circle using the custom function
custom = [Convert(theta) for theta in angles]
x_custom = [custom_elem[0] for custom_elem in custom]
y_custom = [custom_elem[1] for custom_elem in custom]

custom2 = [ConvertDebug(theta) for theta in angles]
x_custom2 = [custom_elem[0] for custom_elem in custom2]
y_custom2 = [custom_elem[1] for custom_elem in custom2]


#Also plot some key points
specific_custom_coordinates = [Convert(theta) for theta in specific_angles]
x_specific_custom, y_specific_custom = zip(*specific_custom_coordinates)

specific_custom_coordinates2 = [ConvertDebug(theta) for theta in specific_angles]
x_specific_custom2, y_specific_custom2 = zip(*specific_custom_coordinates2)

# Plot the unit circle using the custom function
plt.subplot(132)
plt.plot(x_custom, y_custom)
plt.scatter(x_specific_custom, y_specific_custom, marker='o', label='Specific Points')
plt.title('Unit Circle (Custom Function)')
plt.xlabel('z')
plt.ylabel('r')
plt.grid()

# Plot the unit circle using the custom function
plt.subplot(133)
plt.plot(x_custom2, y_custom2)
plt.scatter(x_specific_custom2, y_specific_custom2, marker='o', label='Specific Points')
plt.title('Unit Circle (Custom Function)')
plt.xlabel('w')
plt.ylabel('r')
plt.grid()

print(np.subtract(x_custom, x_custom2))

plt.tight_layout()
plt.show()

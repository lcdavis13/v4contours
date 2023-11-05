import matplotlib.pyplot as plt
import numpy as np

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

# Plot the unit circle using polar coordinates
plt.figure(figsize=(8, 4))
plt.subplot(121)
plt.plot(x_coordinates, y_coordinates)
plt.title('Unit Circle (Polar Coordinates)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()

# Define an undefined custom function to convert polar coordinates to Euclidean coordinates
def Convert(w_deg):
    w_rad = np.radians(w_deg)
    
    def M_deg(w):
        return 716.197 / (71.6197 + w)
    r_deg = M_deg(w_deg)*np.sin(w_rad)
    
    def M_rad(w):
        return 10 / (0.8 + w)
    r_rad = M_rad(w_rad)*np.sin(w_rad)
    
    # Deg and rad versions of M equations (given to me by Dr. Motter) are surprisingly a bit different curves
    
    
    #x = np.cos(np.radians(w))
    #y = np.sin(np.radians(w))
    return w_rad, r_rad

# Create lists to store the x and y coordinates of the points on the unit circle using the custom function
x_custom = [Convert(theta)[0] for theta in angles]
y_custom = [Convert(theta)[1] for theta in angles]

# Plot the unit circle using the custom function
plt.subplot(122)
plt.plot(x_custom, y_custom)
plt.title('Unit Circle (Custom Function)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()

plt.tight_layout()
plt.show()

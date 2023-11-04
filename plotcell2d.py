import matplotlib.pyplot as plt
import numpy as np

# Load data from the file
file_path = 'data/KBA.XY'
data = np.loadtxt(file_path)

# Separate X, Y, and ID columns
X = data[:, 0]
Y = data[:, 1]
ID = data[:, 2]

# Find unique IDs
unique_ids = np.unique(ID)

# Create a color map for different contours
cmap = plt.get_cmap('viridis')

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Plot each contour
for i, unique_id in enumerate(unique_ids):
    mask = (ID == unique_id)
    x_contour = X[mask]
    y_contour = Y[mask]
    color = cmap(i / len(unique_ids))  # Assign a color based on the contour number
    ax.plot(x_contour, y_contour, label=f'Contour {unique_id}', color=color)

# Set labels and legend
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()

# Show the plot
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Initialize variables to store data
contours = []
current_contour = []

# Read the data from the file and process it
with open("data/GAJ.XY", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            x, y, depth = map(float, line.split())
            current_contour.append((x, y, depth))
        else:
            if current_contour:
                contours.append(current_contour)
            current_contour = []

# Create a dictionary to store contours by depth
contours_by_depth = {}
for contour in contours:
    depth = contour[0][2]  # Depth of the contour
    if depth not in contours_by_depth:
        contours_by_depth[depth] = []
    contours_by_depth[depth].append(contour)

# Specify the depths you want to filter and plot
depths_to_plot = [2.0, 3.0, 4.0, 5.0]

# Plot the contours with different colors and labels for specified depths
colors = plt.cm.viridis(np.linspace(0, 1, len(depths_to_plot)))
legend_handles = []
for depth, color in zip(depths_to_plot, colors):
    for contour in contours_by_depth[depth]:
        contour = np.array(contour)
        line, = plt.plot(contour[:, 0], contour[:, 1], color=color)
    legend_handles.append(line)

# Add a custom legend with the appropriate colors
plt.legend(legend_handles, [f"Depth {depth}" for depth in depths_to_plot])

# Set labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Contour Plots')

# Show the plot
plt.show()

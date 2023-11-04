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

# Plot the contours with different colors and labels
colors = plt.cm.viridis(np.linspace(0, 1, len(contours_by_depth)))
legend_labels = set()
for depth, color in zip(contours_by_depth, colors):
    for contour in contours_by_depth[depth]:
        contour = np.array(contour)
        plt.plot(contour[:, 0], contour[:, 1], color=color, label=f"Depth {depth}")
        legend_labels.add(f"Depth {depth}")

# Add a legend with distinct depth entries
plt.legend(labels=legend_labels)

# Set labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Contour Plots')

# Show the plot
plt.show()

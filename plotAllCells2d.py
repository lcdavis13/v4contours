import os
import matplotlib.pyplot as plt
import numpy as np

# Define the folder where your data files are located
folder_path = 'data'

# Create a color map for different contours
cmap = plt.get_cmap('viridis')

# Set the color cycle to ensure distinct colors for each contour
plt.gca().set_prop_cycle(color=[cmap(i) for i in np.linspace(0, 1, len(os.listdir(folder_path)))])

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# List of desired depths as integers
desired_depths = [2, 3, 4]

# Iterate over files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.XY'):
        file_path = os.path.join(folder_path, filename)
        data = np.loadtxt(file_path)
        X = data[:, 0]
        Y = data[:, 1]
        depth = data[:, 2]

        # Convert depth values to integers
        depth = depth.astype(int)

        for d in np.unique(depth):
            if d in desired_depths:
                # Create a unique label for the contour
                unique_label = f'{filename}_{d}'

                # Filter data points based on the depth
                mask = (depth == d)
                X_contour = X[mask]
                Y_contour = Y[mask]

                # Plot the contour with a unique label
                ax.plot(X_contour, Y_contour, label=unique_label)

# Set labels and legend after plotting all contours
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend(loc='upper right')

# Show the plot
plt.show()


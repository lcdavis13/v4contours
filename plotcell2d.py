import math
import os
import random

import matplotlib.pyplot as plt
import numpy as np

def read_contours_from_file(file_path):
    contours = []
    current_contour = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                x, y, depth = map(float, line.split())
                current_contour.append((x, y, depth))
            else:
                if current_contour:
                    contours.append(current_contour)
                current_contour = []

    return contours

def organize_contours_by_depth(contours):
    contours_by_depth = {}
    for contour in contours:
        depth = contour[0][2]  # Depth of the contour
        if depth not in contours_by_depth:
            contours_by_depth[depth] = []
        contours_by_depth[depth].append(contour)

    return contours_by_depth

def plot_contours_with_depths(contours_by_depth, depths_to_plot, legend_handles, plot_mirrors_too=True):
    colors = plt.cm.viridis(np.linspace(0, 1, len(depths_to_plot)))
    for depth, color in zip(depths_to_plot, colors):
        contours_at_depth = contours_by_depth.get(depth, [])
        if contours_at_depth:
            for contour in contours_at_depth:
                contour = np.array(contour)
                linewidth = 5.0*math.log(depth)
                gapwidth = 5.0/math.log(depth)
                line, = plt.plot(contour[:, 0], contour[:, 1], color=color, ls=(0, (linewidth, gapwidth)))
                if plot_mirrors_too:
                    line, = plt.plot(-contour[:, 0], contour[:, 1], color=color, ls=(0, (linewidth, gapwidth)))
            legend_handles.append(line)
        
def plot_contour_centers(contours_by_depth, depths_to_plot, legend_handles, plot_mirrors_too=True):
    colors = plt.cm.viridis(np.linspace(0, 1, len(depths_to_plot)))
    for depth, color in zip(depths_to_plot, colors):
        contours_at_depth = contours_by_depth.get(depth, [])
        if contours_at_depth:
            for contour in contours_by_depth[depth]:
                contour = np.array(contour)
                center = np.mean(contour[:, 0:2], axis=0)
                line, = plt.plot(center[0], center[1], color=color, marker='o')
                if plot_mirrors_too:
                    line, = plt.plot(-center[0], center[1], color=color, marker='o')
            legend_handles.append(line)

def plot_file(file_path, depths_to_plot, legend_handles, plot_mirrors_too=True):
    contours = read_contours_from_file(file_path)
    contours_by_depth = organize_contours_by_depth(contours)
    
    plot_contours_with_depths(contours_by_depth, depths_to_plot, legend_handles, plot_mirrors_too)
    #plot_contour_centers(contours_by_depth, [8.0], legend_handles, plot_mirrors_too)
    
    
def plot_all_files(folder_path, ext, depths_to_plot, legend_handles, plot_mirrors_too=True):
    for filename in os.listdir(folder_path):
        if filename.endswith(ext) :# and ((filename.startswith('Q') or filename.startswith('R') or filename.startswith('S')) and random.Random().randint(0, 1000) < 10):
            file_path = os.path.join(folder_path, filename)
            plot_file(file_path, depths_to_plot, legend_handles, plot_mirrors_too)
            
            
def add_target_rings(num_rings):
    radmult = 2
    # Adding concentric circles with dashed black lines
    theta = np.linspace(0, 2 * np.pi, 100)  # Points around the circle
    for i in range(1, num_rings + 1):
        x = i * np.cos(theta) * radmult
        y = i * np.sin(theta) * radmult
        plt.plot(x, y, color='pink', linestyle='dashed', linewidth=1.5)
        

    
def show_plots(legend_handles, depths_to_plot):
    plt.legend(legend_handles, [f"Depth {depth}" for depth in depths_to_plot], loc='upper left')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('V4 Receptive Fields')
    plt.axis('equal')
    plt.show()


if __name__ == "__main__":
    depths_to_plot = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0] #[2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    legend_handles = []
    
    #plot_file('data/JDK.XY', depths_to_plot, legend_handles)
    plot_all_files('data', '.XY', depths_to_plot, legend_handles, plot_mirrors_too=False)
    add_target_rings(10)

    show_plots(legend_handles, depths_to_plot)
    
    # ToDo use two legends, one for linestyle (depth) and one for color (cell): https://stackoverflow.com/questions/12761806/matplotlib-2-different-legends-on-same-graph
    # ToDo if centroid is on right of y axis, mirror the contour

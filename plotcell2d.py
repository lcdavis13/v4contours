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

def plot_contours_with_depths(contours_by_depth, depths_to_plot, legend_handles):
    colors = plt.cm.viridis(np.linspace(0, 1, len(depths_to_plot)))
    for depth, color in zip(depths_to_plot, colors):
        for contour in contours_by_depth[depth]:
            contour = np.array(contour)
            line, = plt.plot(contour[:, 0], contour[:, 1], color=color, ls=(0, (5, 20.0/depth)))
        legend_handles.append(line)

def plot_file(file_path, depths_to_plot, legend_handles):
    contours = read_contours_from_file(file_path)
    contours_by_depth = organize_contours_by_depth(contours)
    
    plot_contours_with_depths(contours_by_depth, depths_to_plot, legend_handles)
    
def show_plots(legend_handles, depths_to_plot):
    plt.legend(legend_handles, [f"Depth {depth}" for depth in depths_to_plot])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Contour Plots')
    plt.show()


if __name__ == "__main__":
    depths_to_plot = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    legend_handles = []
    
    plot_file("data/GBE.XY", depths_to_plot, legend_handles)
    plot_file("data/GAJ.XY", depths_to_plot, legend_handles)

    show_plots(legend_handles, depths_to_plot)
    

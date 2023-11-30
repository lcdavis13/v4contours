import os
import numpy as np
import pandas as pd
from math import atan2, degrees, radians

def polar_coordinates(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = atan2(y, x)
    return r, theta

def rotate_coordinates(x, y, angle):
    x_rotated = x * np.cos(angle) - y * np.sin(angle)
    y_rotated = x * np.sin(angle) + y * np.cos(angle)
    return x_rotated, y_rotated

def process_file(input_folder, output_folder, filename, threshold=8):
    # Read the file
    file_path = os.path.join(input_folder, filename)
    df = pd.read_csv(file_path, header=None, names=['X', 'Y', 'Depth'])

    # Convert 'X' and 'Y' columns to numeric
    df['X'] = pd.to_numeric(df['X'], errors='coerce')
    df['Y'] = pd.to_numeric(df['Y'], errors='coerce')

    # Drop rows with NaN values
    df = df.dropna(subset=['X', 'Y'])

    # Filter rows based on depth threshold
    filtered_df = df[df['Depth'] > threshold]

    # Calculate average X and Y
    avg_x = np.mean(filtered_df['X'])
    avg_y = np.mean(filtered_df['Y'])

    # Calculate polar coordinates
    r, theta = polar_coordinates(avg_x, avg_y)

    # Rotate coordinates
    df['X'], df['Y'] = rotate_coordinates(df['X'], df['Y'], -theta)

    # Write the modified data to a new file
    output_filename = os.path.splitext(filename)[0] + '_rotated' + os.path.splitext(filename)[1]
    output_path = os.path.join(output_folder, output_filename)
    df.to_csv(output_path, index=False, sep='\t')  # adjust delimiter as needed

    return r, degrees(theta), filename


def main(input_folder, output_folder, polar_file, threshold=8):
    result_list = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".XY"):
            polar_coords = process_file(input_folder, output_folder, filename, threshold)
            result_list.append(polar_coords)

    # Write CSV file with polar coordinates and original file names
    pd.DataFrame(result_list, columns=['Radius', 'Theta', 'Filename']).to_csv(polar_file, index=False)

if __name__ == "__main__":
    input_folder = "../data"
    output_folder = "../data_rotated"
    polar_file = "../polar_coordinates.csv"
    threshold_value = 8
    main(input_folder, output_folder, polar_file, threshold_value)

import os

import numpy as np
import pandas as pd

def find_largest_and_smallest(folder_path):
    # Initialize variables to store the overall largest and smallest values
    max_x = float('-inf')
    max_y = float('-inf')
    min_x = float('inf')
    min_y = float('inf')
    max_r = float('-inf')
    min_theta = float('inf')
    max_theta = float('-inf')

    try:
        # Iterate through all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".XY"):
                file_path = os.path.join(folder_path, filename)

                # Read the file into a pandas DataFrame
                df = pd.read_csv(file_path, delim_whitespace=True, header=None, names=['x', 'y', 'depth'])
                df['r'] = (df['x']**2 + df['y']**2)**0.5
                df['theta'] = np.arctan2(df['y'], df['x'])

                # Update overall largest and smallest values
                max_x = max(max_x, df['x'].max())
                max_y = max(max_y, df['y'].max())
                min_x = min(min_x, df['x'].min())
                min_y = min(min_y, df['y'].min())
                max_r = max(max_r, df['r'].max())
                min_theta = min(min_theta, df['theta'].min())
                max_theta = max(max_theta, df['theta'].max())

        # Return the results
        return max_r, max_x, max_y, min_x, min_y, min_theta, max_theta

    except FileNotFoundError:
        print("Folder not found:", folder_path)
        return None


# Example usage
folder_path = '../data'  # Replace with the actual path to your folder
result = find_largest_and_smallest(folder_path)

# Print the results outside the function
if result is not None:
    max_r, max_x, max_y, min_x, min_y, min_theta, max_theta = result
    print("max r:", max_r)
    print("min x", min_x)
    print("max x:", max_x)
    print("min y", min_y)
    print("max y", max_y)
    print("min theta", min_theta)
    print("max theta", max_theta) # these measures are pretty meaningless since the angles loop. If there is a range less than -pi to pi, this probably won't find it. And it's unlikely to exist in the data anyway.

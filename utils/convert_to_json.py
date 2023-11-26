import os
import json

def read_contours_from_file(file_path):
    contours = {}
    current_contour = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                x, y, depth = map(float, line.split())
                depth = int(depth)
                current_contour.append({'x': x, 'y': y, 'depth': depth})
            else:
                if current_contour:
                    if depth not in contours:
                        contours[depth] = []
                    contours[depth].append(current_contour)
                    current_contour = []

    return contours

def convert_directory_to_json(directory_path, output_file):
    data = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.XY'):
            file_path = os.path.join(directory_path, filename)
            contours = read_contours_from_file(file_path)
            data[filename] = contours

    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)


convert_directory_to_json('../data', '../data.json')
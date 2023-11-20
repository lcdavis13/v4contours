import math

import plotly.express
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np


def getV1Mag2D(dtheta = math.pi/180.0):
    #angles = np.multiply([0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0, 60.0, 80.0, 89.0], math.pi/180.0)
    angles = np.arange(0.0, math.pi / 2.0, dtheta)
    
    def calc_m(w):
        # return 716.197 / (71.6197 + w) # radians version from Brad
        # return 10 / (0.8 + w)  # degrees version from Brad
        return 525.6 / (1.0 + 33.48 * w)  # 1984 radians version
    
    # Define an undefined custom function to convert polar coordinates to Euclidean coordinates
    def calc_r(w, m):
        return m * np.sin(w)
        # might need to ensure these are zero when w is zero
    
    def calc_delta_z(m, r):
        dr_dw = np.diff(r) / dtheta  # w is theta; dw is dtheta
        dr_dw = np.append(dr_dw, dr_dw[-1])  # diff loses one element, duplicate last derivative to preserve length
        m_sqr = np.square(m)
        dr_dw_sqr = np.square(dr_dw)
        sqr_dif = np.subtract(m_sqr, dr_dw_sqr)
        return np.sqrt(sqr_dif)
    
    # Define an undefined custom function to convert polar coordinates to Euclidean coordinates
    def calc_z(delta_z):
        return np.cumsum(delta_z) * dtheta
    
    m = calc_m(angles)
    r = calc_r(angles, m)
    delta_z = calc_delta_z(m, r)
    z = calc_z(delta_z)
    
    zeros = np.zeros((len(z)), dtype=np.float32)
    return np.column_stack([z, r, zeros])


def Rx(theta):
    return np.matrix([[1, 0, 0],
                      [0, math.cos(theta), -math.sin(theta)],
                      [0, math.sin(theta), math.cos(theta)]])

    

curve = getV1Mag2D()

def rotate_around_x_axis(points, num_rotations):
    """
    Rotate a list of 3D points around the X-axis multiple times.

    Parameters:
    - points (list of tuples): List of 3D points (x, y, z).
    - num_rotations (int): Number of rotations around the X-axis.

    Returns:
    - list of list of tuples: List of rotated curves.
    """
    points = np.array(points)
    rotated_curves = []

    for rotation in range(num_rotations):
        # Define rotation matrix around X-axis
        theta = 2 * np.pi * rotation / num_rotations
        rotation_matrix = Rx(theta)

        # Apply rotation to points
        rotated_points = np.dot(points, rotation_matrix.T)
        rotated_curves.append(rotated_points.tolist())

    return rotated_curves

def plot_rotated_curves(rotated_curves):
    """
    Plot rotated curves using Plotly.

    Parameters:
    - rotated_curves (list of list of tuples): List of rotated curves.
    """
    fig = go.Figure()

    for curve in rotated_curves:
        x, y, z = zip(*curve)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines'))

    fig.update_layout(scene=dict(aspectmode="data"))
    fig.write_html("renders/v1magCurves.html", auto_open=True)
    
num_rotations = 8

rotated_curves = rotate_around_x_axis(curve, num_rotations)
plot_rotated_curves(rotated_curves)

def create_mesh(rotated_curves):
    """
    Create a mesh from the triangulation of rotated curves.

    Parameters:
    - rotated_curves (list of list of tuples): List of rotated curves.

    Returns:
    - plotly.graph_objects.Figure: Plotly figure displaying the mesh.
    """
    vertices = np.concatenate(rotated_curves, axis=0)

    # Create triangulation
    num_points_per_curve = len(rotated_curves[0])
    faces = []
    for i in range(len(rotated_curves) - 1):
        next_i = (i + 1) % len(rotated_curves)
        for j in range(num_points_per_curve - 1):
            current = i * num_points_per_curve + j
            next_row = next_i * num_points_per_curve + j
            faces.extend([[current, current + 1, next_row], [current + 1, next_row + 1, next_row]])

    mesh = go.Figure(ff.create_trisurf(x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2], simplices=faces))
    mesh.update_layout(scene=dict(aspectmode="data"))
    return mesh

mesh_fig = create_mesh(rotated_curves)
mesh_fig.write_html("renders/v1magMesh.html", auto_open=True)


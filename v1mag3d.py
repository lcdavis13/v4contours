import math

import plotly.graph_objects as go
import numpy as np


def getV1Mag2D(dtheta = math.pi/180.0):
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


def Ry(theta):
    return np.matrix([[math.cos(theta), 0, math.sin(theta)],
                      [0, 1, 0],
                      [-math.sin(theta), 0, math.cos(theta)]])


def Rz(theta):
    return np.matrix([[math.cos(theta), -math.sin(theta), 0],
                      [math.sin(theta), math.cos(theta), 0],
                      [0, 0, 1]])


def getV1Mag3D(curve2d, dphi = math.pi/10.0):
    angles = np.arange(0.0, math.pi * 2.0, dphi)
    
    ptcloud = np.empty((0, 3), dtype=np.float32)
    for phi in angles:
        pts = curve2d.copy()
        #scipy.spatial.transformath.Rotation.from_euler('x', phi, degrees=False).as_matrix()
        transform_matrix = Rx(phi)
        pts_dot = pts.dot(transform_matrix.T)
        #pts_rot = np.ndarray(pts_dot)
        ptcloud = np.concatenate((ptcloud, pts_dot))
    
    return ptcloud
    

curve = getV1Mag2D()
pts = getV1Mag3D(curve)

x, y, z = pts.T

fig = go.Figure(data=[go.Mesh3d(x=x[0], y=y[0], z=z[0], color='lightpink', opacity=0.50)])
fig.show()
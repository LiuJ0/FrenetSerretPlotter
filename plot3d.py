import numpy as np
from calculate_TNB import calculateTNB


def make_curve(t, curve, start, end):
    data = np.linspace(start, end, int((end - start) * 5))
    x, y, z = curve.eval(t, data).x, curve.eval(t, data).y, curve.eval(t, data).z
    T, N, B = calculateTNB(t, curve, data)
    return np.vstack((x, y, z)), T, N, B


def get_bounds(curve):
    x_min, x_max = min(curve[0]) * 0.9, max(curve[0]) * 1.1
    y_min, y_max = min(curve[1]) * 0.9, max(curve[1]) * 1.1
    z_min, z_max = min(curve[2]) * 0.9, max(curve[2]) * 1.1
    return x_min, x_max, y_min, y_max, z_min, z_max


def set_bounds(ax, curve):
    x_min, x_max, y_min, y_max, z_min, z_max = get_bounds(curve)
    ax.set(xlim3d=(x_min, x_max), xlabel='X')
    ax.set(ylim3d=(y_min, y_max), ylabel='Y')
    ax.set(zlim3d=(z_min, z_max), zlabel='Z')

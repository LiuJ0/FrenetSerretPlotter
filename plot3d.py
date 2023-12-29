def get_bounds(curve):
    if not min(curve[0]) == min(curve[0]):
        x_min, x_max = min(curve[0]) * 0.9, max(curve[0]) * 1.1
    else:
        x_min, x_max = float(min(curve[0]) - 1), float(max(curve[0]) + 1)
    if not min(curve[1]) == min(curve[1]):
        y_min, y_max = min(curve[1]) * 0.9, max(curve[1]) * 1.1
    else:
        y_min, y_max = float(min(curve[1]) - 1), float(max(curve[1]) + 1)
    if not min(curve[2]) == min(curve[2]):
        z_min, z_max = min(curve[2]) * 0.9, max(curve[2]) * 1.1
    else:
        z_min, z_max = float(min(curve[2]) - 1), float(max(curve[2]) + 1)
    return x_min, x_max, y_min, y_max, z_min, z_max


def set_bounds(ax, curve):
    x_min, x_max, y_min, y_max, z_min, z_max = get_bounds(curve)
    ax.set(xlim3d=(x_min, x_max), xlabel='X')
    ax.set(ylim3d=(y_min, y_max), ylabel='Y')
    ax.set(zlim3d=(z_min, z_max), zlabel='Z')


def calculate_scale_factor(curve):
    x_min, x_max, y_min, y_max, z_min, z_max = get_bounds(curve)
    max_bounds = max(x_max - x_min, y_max - y_min, z_max - z_min)
    x_scale = (x_max - x_min) / max_bounds
    y_scale = (y_max - y_min) / max_bounds
    z_scale = (z_max - z_min) / max_bounds
    return x_scale, y_scale, z_scale

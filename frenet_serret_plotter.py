import matplotlib.pyplot as plt
from matplotlib import animation
from calculate_TNB import ParametricCurve, make_curve, calculate_curvatures
from sympy import *
from plot3d import *
import numpy as np
from latex2sympy2 import latex2sympy
import argparse


def get_arrow(curve, V, num):
    return curve[0, num], curve[1, num], curve[2, num], V[0, num], V[1, num], V[2, num]


def update(num, curve, curve_plot, T, N, B, curvature, torsion):
    curve_plot.set_data(curve[:2, :num])
    curve_plot.set_3d_properties(curve[2, :num])
    global T_plot
    global N_plot
    global B_plot
    T_plot.remove()
    N_plot.remove()
    B_plot.remove()
    T_plot = ax.quiver(*get_arrow(curve, T, num), color='r', label='Tangent')
    N_plot = ax.quiver(*get_arrow(curve, N, num), color='g', label='Normal')
    B_plot = ax.quiver(*get_arrow(curve, B, num), color='b', label='Binormal')
    ax.text(0, 0, 0, f"Curvature: {curvature[0, num]}\nTorsion: {torsion[0, num]}")
    return curve_plot, T_plot, N_plot, B_plot


"""start = 0
end = 2*np.pi
num = int((end - start) * 20)
t = Symbol('t')"""

# Helix: r'\cos{t}', r'\sin{t}', r't'
# Circle: r'\cos{t}', r'\sin{t}', r'0'
# Thing 1: r'\sin{3t}\cos{5t}', r'\sin{3t}\sin{5t}', r'\cos{3t}'
# Thing 2: r'\frac{\sin{2t}}{t^2 + 4}', r'\frac{\cos{2t}}{t^2 + 4}', r'\frac{t - \pi}{10}'
# Trefoil knot: r'\cos{t} + 2\cos{2t}', r'\sin{t} - 2\sin{2t}', r'-\sin{3t}'
# Another helix: r'\cos{t^3}', r'\sin{t^3}', r't^3'
x_tex, y_tex, z_tex = r'\cos{t}', r'\sin{t}', r't'
save_file = 'output/helix.gif'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=str, default=r'\cos{t}')
    parser.add_argument('--y', type=str, default=r'\sin{t}')
    parser.add_argument('--z', type=str, default=r't')
    parser.add_argument('--start', type=float, default=0)
    parser.add_argument('--end', type=float, default=2*np.pi)
    parser.add_argument('--num', type=int, default=100)
    parser.add_argument('--fps', type=int, default=15)
    parser.add_argument('--save', type=str, default='output/helix.gif')
    t = Symbol('t')
    args = parser.parse_args()
    x = ParametricCurve(latex2sympy(args.x), latex2sympy(args.y), latex2sympy(args.z))
    data = np.linspace(args.start, args.end, args.num)
    curve, T, N, B = make_curve(data, t, x)
    curvature, torsion = calculate_curvatures(t, x, data)
    x_scale, y_scale, z_scale = calculate_scale_factor(curve)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    set_bounds(ax, curve)

    curve_plot = ax.plot([], [], [], lw=2)[0]
    T_plot = ax.quiver(*get_arrow(curve, T, 0), color='r', label='Tangent')
    N_plot = ax.quiver(*get_arrow(curve, N, 0), color='g', label='Normal')
    B_plot = ax.quiver(*get_arrow(curve, B, 0), color='b', label='Binormal')

    ani = animation.FuncAnimation(
        fig, update, args.num, fargs=(curve, curve_plot, T, N, B, curvature, torsion), interval=1)

    ani.save('output/helix.gif', writer='Pillow', fps=args.fps)

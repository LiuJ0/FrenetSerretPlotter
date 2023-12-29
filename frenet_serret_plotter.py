import matplotlib.pyplot as plt
from matplotlib import animation
from calculate_TNB import ParametricCurve, make_curve, calculate_curvatures
from sympy import *
from plot3d import *
import numpy as np
from latex2sympy2 import latex2sympy
import argparse
import codecs
import sys


def get_viewing_angle(key):
    match key:
        case 'XY':
            return 90, -90, 0
        case 'XZ':
            return 0, -90, 0
        case 'YZ':
            return 0, 0, 0
        case '-XZ':
            return 0, 90, 0
        case '-YZ':
            return 0, 180, 0
        case '-XY':
            return -90, 90, 0
        case _:
            return 30, 45, 15

def unescaped_str(s):
    return str(s).encode('utf-8').decode('unicode_escape').replace('-', '-1*')

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
    curvature_label.set_text(f"{curvature[num]}\n{torsion[num]}")
    return curve_plot, T_plot, N_plot, B_plot, curvature_label


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
    for i, arg in enumerate(sys.argv):
        if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--x', type=str, default=r'\cos{t}', help="The x component of the parametric curve.")
    parser.add_argument('-y', '--y', type=str, default=r'\sin{t}', help="The y component of the parametric curve.")
    parser.add_argument('-z', '--z', type=str, default=r't', help="The z component of the parametric curve.")
    parser.add_argument('-s', '--start', type=float, default=0, help="When the curve starts.")
    parser.add_argument('-e', '--end', type=float, default=2*np.pi, help="When the curve ends.")
    parser.add_argument('-n', '--num', type=int, default=100, help="The number of points to plot. If your curve looks "
                                                                   "jagged, increase this number.")
    parser.add_argument('-f', '--fps', type=int, default=15, help="The number of frames per second. Change this to "
                                                                  "slow down or speed up the animation.")
    parser.add_argument('-o', '--output', type=str, default='output/helix.gif', help="The output file name.")
    parser.add_argument('-a', '--angle', type=str, default=None, help="The viewing angle. Options are XY, XZ, YZ, "
                                                                      "-XZ, -YZ, -XY, or a bird's eye view (default).")
    t = Symbol('t')
    args = parser.parse_args()
    args = parser.parse_args(['--x', '\cos{t} + 2\cos{2t}', '--y', '\sin{t} - 2\sin{2t}', '--z', ' -\sin{3t}', '--output', 'output/helix.gif'])
    print(args)
    x = ParametricCurve(latex2sympy(unescaped_str(args.x)), latex2sympy(unescaped_str(args.y)), latex2sympy(unescaped_str(args.z)))
    data = np.linspace(latex2sympy(unescaped_str(args.start)).evalf(), latex2sympy(unescaped_str(args.end)).evalf(), args.num)
    curve, T, N, B = make_curve(data, t, x)
    curvature, torsion = calculate_curvatures(t, x, data)
    x_scale, y_scale, z_scale = calculate_scale_factor(curve)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x_min, x_max, y_min, y_max, z_min, z_max = get_bounds(curve)
    base_label = plt.gcf().text(0.05, 0.90, "Curvature: \nTorsion: ")
    curvature_label = plt.gcf().text(0.175, 0.90, f"{curvature[0]}\n{torsion[0]}", font='monospace')
    set_bounds(ax, curve)

    curve_plot = ax.plot([], [], [], lw=2)[0]
    T_plot = ax.quiver(*get_arrow(curve, T, 0), color='r', label='Tangent')
    N_plot = ax.quiver(*get_arrow(curve, N, 0), color='g', label='Normal')
    B_plot = ax.quiver(*get_arrow(curve, B, 0), color='b', label='Binormal')

    if args.angle:
        ax.view_init(*get_viewing_angle(args.angle))
    ani = animation.FuncAnimation(
        fig, update, args.num, fargs=(curve, curve_plot, T, N, B, curvature, torsion), interval=1)

    ani.save(args.output, writer='Pillow', fps=args.fps)

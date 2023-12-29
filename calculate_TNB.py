from sympy import *
import numpy as np
from plot3d import calculate_scale_factor


class npVector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return npVector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return npVector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float):
        return npVector(self.x * other, self.y * other, self.z * other)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def proj(self, other):
        """
        :param other: npVector
        :return: proj_{other} self
        A simplified formula is used because other is a unit vector. (Note that T.T = 1)
        """
        return (other) * self.dot(other)

    def cross(self, other):
        return npVector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                        self.x * other.y - self.y * other.x)

    def norm(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** (1 / 2)

    def to_vstack(self):
        return np.vstack((self.x, self.y, self.z))


class ParametricCurve:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def diff(self):
        return ParametricCurve(self.x.diff(), self.y.diff(), self.z.diff())

    def eval(self, t, data):
        if not self.x.is_constant():
            xl = lambdify(t, self.x, "numpy")(data)
        else:
            xl = np.full((1, len(data)), self.x)
        if not self.y.is_constant():
            yl = lambdify(t, self.y, "numpy")(data)
        else:
            yl = np.full((1, len(data)), self.y)
        if not self.z.is_constant():
            zl = lambdify(t, self.z, "numpy")(data)
        else:
            zl = np.full((1, len(data)), self.z)
        return npVector(xl, yl, zl)


def calculateTNB(t, x, data):
    """
    :param x: Curve
    :return: T, N, B
    """
    xd = x.diff().eval(t, data)
    xdd = x.diff().diff().eval(t, data)
    T = xd * (1 / xd.norm())
    N = (xdd - xdd.proj(T)) * (1 / (xdd - xdd.proj(T)).norm())
    B = T.cross(N)
    # assert normal(T, N, B)
    # assert orthogonal(T, N, B)
    return T.to_vstack(), N.to_vstack(), B.to_vstack()


def calculate_curvatures(t, x, data):
    """
    :param x: Curve
    :return: curvature, torsion
    """
    xd = x.diff().eval(t, data)
    xdd = x.diff().diff().eval(t, data)
    xddd = x.diff().diff().diff().eval(t, data)
    curvature = (xd.cross(xdd)).norm() / (xd.norm() ** 3)
    # curvature_diff = [""] + ["(increasing)" if (x >= 0) else "(decreasing)" for x in np.diff(curvature)]
    torsion = (xd.cross(xdd)).dot(xddd) / (xd.norm() ** 6 * curvature ** 2)
    # torsion_diff = [""] + ["(increasing)" if (x >= 0) else "(decreasing)" for x in np.diff(torsion)]
    return curvature.round(4), torsion.round(4)


def normal(T, N, B):
    return False if T.norm().all() != 1 or N.norm().all() != 1 or B.norm().all() != 1 else True


def orthogonal(T, N, B):
    """
    :param T: npVector
    :param N: npVector
    :param B: npVector
    :return: T, N, B
    """
    return False if T.dot(N).all() != 0 or T.dot(B).all() != 0 or N.dot(B).all() != 0 else True


def make_curve(data, t, curve, scaled=True):
    x, y, z = curve.eval(t, data).x, curve.eval(t, data).y, curve.eval(t, data).z
    T, N, B = calculateTNB(t, curve, data)
    if scaled:
        x_scale, y_scale, z_scale = calculate_scale_factor(np.vstack((x, y, z)))
        T[0] *= x_scale
        T[1] *= y_scale
        T[2] *= z_scale
        N[0] *= x_scale
        N[1] *= y_scale
        N[2] *= z_scale
        B[0] *= x_scale
        B[1] *= y_scale
        B[2] *= z_scale
    return np.vstack((x, y, z)), T, N, B

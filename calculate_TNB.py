from sympy import *
import numpy as np


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

    def diff(self):
        return ParametricCurve(self.x.diff(), self.y.diff(), self.z.diff())

    def eval(self, t, data):
        xl = lambdify(t, self.x, "numpy")
        yl = lambdify(t, self.y, "numpy")
        zl = lambdify(t, self.z, "numpy")
        return npVector(xl(data), yl(data), zl(data))


def calculateTNB(t, x, data):
    """
    :param x: Curve
    :return: T, N, B
    """
    xd = x.diff().eval(t, data)
    xdd = x.diff().diff().eval(t, data)
    xddd = x.diff().diff().diff().eval(t, data)
    # print(xd)
    # print(xdd)
    T = xd * (1 / xd.norm())
    N = (xdd - xdd.proj(T)) * (1 / (xdd - xdd.proj(T)).norm())
    B = T.cross(N)
    assert normalized(T, N, B)
    return T.to_vstack(), N.to_vstack(), B.to_vstack()


def normalized(T, N, B):
    return False if T.norm().all() != 1 or N.norm().all() != 1 or B.norm().all() != 1 else True


def orthogonal(T, N, B):
    """
    :param T: npVector
    :param N: npVector
    :param B: npVector
    :return: T, N, B
    """
    return False if T.dot(N).all() != 0 or T.dot(B).all() != 0 or N.dot(B).all() != 0 else True

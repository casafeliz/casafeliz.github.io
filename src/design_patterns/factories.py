"""
Design Patterns : Factories
"""
from enum import Enum
from math import cos, sin


class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2


class Point1:
    def __init__(self, a, b, system=CoordinateSystem.CARTESIAN):
        if system == CoordinateSystem.CARTESIAN:
            self.x = a
            self.y = b
        elif system == CoordinateSystem.POLAR:
            self.x = a * cos(b)
            self.y = a * sin(b)

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"


class Point2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"

    @staticmethod
    def new_cartesian_point(x, y):
        return Point2(x, y)

    @staticmethod
    def new_polar_point(rho, theta):
        return Point2(rho * cos(theta), rho * sin(theta))


class Point3:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"

    class PointFactory:
        @staticmethod
        def new_cartesian_point(x, y):
            return Point3(x, y)

        @staticmethod
        def new_polar_point(rho, theta):
            return Point3(rho * cos(theta), rho * sin(theta))

    factory = PointFactory()


if __name__ == "__main__":
    p_cartesian = Point1(2, 3, CoordinateSystem.CARTESIAN)
    p_polar = Point1(1, 2, CoordinateSystem.POLAR)
    print(p_cartesian, p_polar)
    p1 = Point2.new_cartesian_point(2, 3)
    p2 = Point2.new_polar_point(1, 2)
    print(p1, p2)
    p3 = Point3.factory.new_cartesian_point(2, 3)
    p4 = Point3.factory.new_polar_point(1, 2)
    print(p3, p4)

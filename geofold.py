# Python Implementation of Geofold, the 2D geometry solver

import math


class Point:
    def __init__(self, x, y):
        self.c = complex(x, y)

    def __str__(self):
        return 'Point({}, {})'.format(self.c.real, self.c.imag)

    def __eq__(self, other):
        return self.c == other.c

    def __hash__(self):
        return hash(self.c)

    def __repr__(self):
        return str(self)

    # Logic
    @property
    def x(self):
        return self.c.real

    @property
    def y(self):
        return self.c.imag

    def dist_pt(self, other):
        return abs(self.c - other.c)

    def dist_line(self, line):
        return abs(line.project(self)) / math.sqrt(line.slope ** 2 + 1)


class Line:
    def __init__(self, slope, intercept):
        self.slope = slope
        self.intercept = intercept
        # y = mx + b
        # x = (y - b) / m
        # mx - y + b = 0

    def __str__(self):
        return 'Line y = {}x + {}'.format(self.slope, self.intercept)

    def __eq__(self, other):
        return self.slope == other.slope and self.intercept == other.intercept

    def __hash__(self):
        return hash((self.slope, self.intersect))

    def __repr__(self):
        return str(self)

    # Logic
    def project(self, point):
        return self.slope * point.x - point.y + self.intercept

    def at_x(self, x):
        return self.slope * x + self.intercept

    def at_y(self, y):
        return (y - self.intercept) / self.slope

    def intersect(self, other):
        if type(other) == Line:
            if self.slope == other.slope:
                return None
            # ax + b = cx + d
            # x = (d - b) / (a - c)
            x = (other.intercept - self.intercept) / (self.slope - other.slope)
            y = self.at_x(x)
            return Point(x, y)
        elif type(other) == Segment:
            print("Error: Use line.intersect(segment.line) instead")
            exit(1)
        elif type(other) == Circle:
            A, B, C = self.slope, -1, self.intercept
            h, k, r = other.center.x, other.center.y, other.radius
            a = A ** 2 + B ** 2
            b = 2 * A * C + 2 * A * B * k - 2 * h * B ** 2
            c = C ** 2 + 2 * B * C * k - B ** 2 * (r ** 2 - h ** 2 - k ** 2)
            delta = b ** 2 - 4 * a * c
            if delta < 0:
                return []
            if delta == 0:
                x = -b / (2 * a)
                y = self.at_x(x)
                return [Point(x, y)]
            return sort_two_pts([Point((-b + math.sqrt(delta)) / (2 * a), self.at_x((-b + math.sqrt(delta)) / (2 * a))),
                                 Point((-b - math.sqrt(delta)) / (2 * a), self.at_x((-b - math.sqrt(delta)) / (2 * a)))])

    def perpendicular(self, point):
        return Line(-1 / self.slope, point.y - point.x * -1 / self.slope)

    def parallel(self, point):
        return Line(self.slope, point.y - point.x * self.slope)


def line_from_pts(a, b):
    return Line((b.y - a.y) / (b.x - a.x), a.y - a.x * (b.y - a.y) / (b.x - a.x))


def sort_two_pts(arr):
    if arr[0].x > arr[1].x:
        return [arr[1], arr[0]]
    elif arr[0].x == arr[1].x:
        if arr[0].y > arr[1].y:
            return [arr[1], arr[0]]
    return [arr[0], arr[1]]


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return 'Segment({}, {})'.format(self.p1, self.p2)

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    # Logic
    @property
    def length(self):
        return self.p1.dist_pt(self.p2)

    @property
    def line(self):
        return line_from_pts(self.p1, self.p2)

    @property
    def midpoint(self):
        return Point((self.p1.x + self.p2.x) / 2, (self.p1.y + self.p2.y) / 2)


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __str__(self):
        return 'Circle({}, {})'.format(self.center, self.radius)

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius

    # Logic
    def at_x(self, x):
        delta = self.radius ** 2 - (x - self.center.x) ** 2
        if delta < 0:
            return []
        if delta == 0:
            return [Point(x, self.center.y)]
        return sort_two_pts([Point(x, self.center.y - math.sqrt(delta)),
                             Point(x, self.center.y + math.sqrt(delta))])

    def intersect(self, other):
        if type(other) == Line:
            return other.intersect(self)
        elif type(other) == Segment:
            print("Error: Use circle.intersect(segment.line) instead")
            exit(1)
        elif type(other) == Circle:
            x0, y0, r0 = self.center.x, self.center.y, self.radius
            x1, y1, r1 = other.center.x, other.center.y, other.radius
            d = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            a = (r0**2-r1**2+d**2)/(2*d)
            h = math.sqrt(r0**2-a**2)
            x2 = x0+a*(x1-x0)/d
            y2 = y0+a*(y1-y0)/d
            x3_1 = x2+h*(y1-y0)/d
            y3_1 = y2-h*(x1-x0)/d
            x3_2 = x2-h*(y1-y0)/d
            y3_2 = y2+h*(x1-x0)/d
            if x3_1 == x3_2 and y3_1 == y3_2:
                return [Point(x3_1, y3_1)]
            return sort_two_pts([Point(x3_2, y3_2), Point(x3_1, y3_1)])


ORIGIN = Point(0, 0)

if __name__ == "__main__":
    C1 = Circle(ORIGIN, 200)
    E = Point(200, 0)
    C2 = Circle(E, 180)
    C3 = Circle(E, 108)
    D = C1.intersect(C2)[1]
    K = C3.at_x(D.x)[0]
    L1 = line_from_pts(E, K)
    F = C1.intersect(L1)[0]
    print(F.dist_pt(K))

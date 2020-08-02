import math

import cairo


class Annotation():

    def on_press(self, point):
        pass

    def on_move(self, point):
        pass

    def on_release(self, point):
        pass

    def render(self, cr):
        pass

class MarkerAnnotation(Annotation):

    def __init__(self, line_width=3, rgba=None):
        self.line_width = line_width
        self.rgba = rgba
        self.points = []

    def on_press(self, point):
        self.points.append(point)

    def on_move(self, point):
        self.points.append(point)

    def on_release(self, point):
        self.points.append(point)

    def render(self, cr):
        if self.points:
            cr.set_line_width(self.line_width)
            cr.set_line_join(cairo.LINE_JOIN_BEVEL)
            cr.set_source_rgba(*((0, 0, 0) if self.rgba is None else self.rgba))
            render_path(cr, reduce_path(self.points))
            cr.stroke()

class TextAnnotation(Annotation):

    def __init__(self, default_text='Text', font_size=12, rgba=None):
        self.text = default_text
        self.font_size = font_size
        self.rgba = rgba
        self.origin = None

    def on_press(self, point):
        self.origin = point

    def on_move(self, point):
        self.origin = point

    def render(self, cr):
        if self.origin and self.text:
            cr.set_font_size(self.font_size)
            cr.set_source_rgba(*((0, 0, 0) if self.rgba is None else self.rgba))
            cr.move_to(*self.origin)
            cr.show_text(self.text)
            cr.stroke()

def reduce_path(points):
    reduced = []
    for point in points[:-1]:
        if not reduced or (distance(point, reduced[-1]) > 5):
            reduced.append(point)
    if len(reduced) > 2 and len(points) > 2:
        if distance(reduced[-1], points[-1]) < 5:
            reduced.pop()
    reduced.append(points[-1])
    return reduced

def render_path(cr, points):
    if points:
        cr.move_to(*points[0])
        def p(i):
            return points[i] if 0 <= i < len(points) else None
        for i in range(1, len(points)):
            cs = calc_control_points(p(i - 1), p(i - 2), p(i))
            ce = calc_control_points(p(i), p(i - 1), p(i + 1), True)
            cr.curve_to(*cs, *ce, *p(i))

def calc_control_points(curr_point, prev_point, next_point, reverse=False):
    c = curr_point
    p = prev_point or c
    n = next_point or c
    a = angle(p, n)
    d = distance(p, n)
    rev = math.pi if reverse else 0
    smoothing = 0.2

    x = c[0] + math.cos(a + rev) * d * smoothing
    y = c[1] + math.sin(a + rev) * d * smoothing

    return [x, y]

def distance(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.sqrt(dx ** 2 + dy ** 2)

def angle(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.atan2(dy, dx)

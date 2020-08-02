import math


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
        last_point = self.points[-1]
        if (distance(point, last_point) > 10):
            self.points.append(point)

    def on_release(self, point):
        self.points.append(point)

    def render(self, cr):
        if self.points:
            cr.set_line_width(self.line_width)
            cr.set_source_rgba(*((0, 0, 0) if self.rgba is None else self.rgba))
            cr.move_to(*self.points[0])
            for point in self.points[1:]:
                cr.line_to(*point)
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

def distance(point1, point2):
    dx = math.fabs(point1[0] - point2[0])
    dy = math.fabs(point1[1] - point2[1])
    return math.sqrt(dx ** 2 + dy ** 2)

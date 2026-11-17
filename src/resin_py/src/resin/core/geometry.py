import array
import math

from resin.core.rendering import _fai

# Pre-calculated trigonometry lookup tables
_SIN_TABLE = array.array('h', [int(round(math.sin(math.radians(i)) * 1024)) for i in range(360)])
_COS_TABLE = array.array('h', [int(round(math.cos(math.radians(i)) * 1024)) for i in range(360)])


class StaticBatch:
    def __init__(self):
        self.batch_x = array.array('h', [])
        self.batch_y = array.array('h', [])
        self.batch_w = array.array('h', [])
        self.batch_h = array.array('h', [])
        self.batch_c = array.array('h', [])

    def add(self, rect) -> None:
        if type(rect) is StaticRect:
            self.batch_x.append(int(rect.x))
            self.batch_y.append(int(rect.y))
            self.batch_w.append(int(rect.w))
            self.batch_h.append(int(rect.h))
            self.batch_c.append(int(rect.color))

    def clear(self) -> None:
        del self.batch_x[:]
        del self.batch_y[:]
        del self.batch_w[:]
        del self.batch_h[:]
        del self.batch_c[:]

    def draw(self) -> None:
        _fai.draw_static_batch(self)


class Rect:
    def __init__(self, x: int, y: int, w: int, h: int, color: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.color = color
        self.angle = 0

        self.vertices = array.array('i', [0, 0, 0, 0, 0, 0, 0, 0])
        self.indices = array.array('h', [0, 1, 3, 2])

    def scale(self, factor: float) -> None:
        self.w = self.w * factor
        self.h = self.h * factor

    def rotate(self, degrees: int) -> None:
        self.angle = int(degrees) % 360

    def draw(self) -> None:
        x = int(self.x)
        y = int(self.y)
        w = int(self.w)
        h = int(self.h)

        color = int(self.color)
        angle = int(self.angle) % 360

        if w <= 0 or h <= 0:
            return

        cos_a = _COS_TABLE[angle]
        sin_a = _SIN_TABLE[angle]

        c2x = 2 * x
        c2y = 2 * y

        p1x = (c2x + ((cos_a * (-w) - sin_a * (-h)) >> 10)) >> 1
        p1y = (c2y + ((sin_a * (-w) + cos_a * (-h)) >> 10)) >> 1
        p2x = (c2x + ((cos_a * w - sin_a * (-h)) >> 10)) >> 1
        p2y = (c2y + ((sin_a * w + cos_a * (-h)) >> 10)) >> 1
        p3x = (c2x + ((cos_a * (-w) - sin_a * h) >> 10)) >> 1
        p3y = (c2y + ((sin_a * (-w) + cos_a * h) >> 10)) >> 1
        p4x = (c2x + ((cos_a * w - sin_a * h) >> 10)) >> 1
        p4y = (c2y + ((sin_a * w + cos_a * h) >> 10)) >> 1

        v = self.vertices

        v[0] = int(p1x)
        v[1] = int(p1y)
        v[2] = int(p2x)
        v[3] = int(p2y)
        v[4] = int(p3x)
        v[5] = int(p3y)
        v[6] = int(p4x)
        v[7] = int(p4y)

        _fai.draw_quad(v, self.indices, color)


class StaticRect:
    def __init__(self, x: int, y: int, w: int, h: int, color: int, batch: StaticBatch = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.batch = batch

        if self.batch is not None:
            self.batch.add(self)

    def draw(self) -> None:
        if self.batch is not None:
            self.batch.draw()

        else:
            temp_batch = StaticBatch()
            temp_batch.add(self.x, self.y, self.w, self.h, self.color)
            temp_batch.draw()

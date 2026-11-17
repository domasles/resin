import micropython
import resin_hw


class _FramebufferAccessInterface:
    def __init__(self):
        self.width = resin_hw.WIDTH
        self.height = resin_hw.HEIGHT

    @property
    def buf(self):
        return resin_hw.framebuffer()

    @micropython.viper
    def write_pixel(self, x: int, y: int, color_idx: int):
        width = int(self.width)
        height = int(self.height)
        buf = ptr8(self.buf)

        if 0 <= x < width and 0 <= y < height:
            buf[y * width + x] = color_idx

    def draw_static_batch(self, batch: StaticBatch):
        self._draw_stationary_batch_internal(batch)

    @micropython.viper
    def _draw_stationary_batch_internal(self, batch):
        width = int(self.width)
        height = int(self.height)
        buf = ptr8(self.buf)

        xs = ptr16(batch.batch_x)
        ys = ptr16(batch.batch_y)
        ws = ptr16(batch.batch_w)
        hs = ptr16(batch.batch_h)
        cs = ptr16(batch.batch_c)
        n = int(len(batch.batch_x))

        i = 0

        while i < n:
            x = int(xs[i])
            y = int(ys[i])
            w = int(ws[i])
            h = int(hs[i])
            color_idx = int(cs[i])

            if w > 0 and h > 0:
                x2 = x + w
                y2 = y + h

                if not (x2 <= 0 or x >= width or y2 <= 0 or y >= height):
                    if x < 0:
                        x = 0

                    if x2 > width:
                        x2 = width

                    if y < 0:
                        y = 0

                    if y2 > height:
                        y2 = height

                    if x < x2 and y < y2:
                        cy = y

                        while cy < y2:
                            row_offset = cy * width
                            cx = x

                            while cx < x2:
                                buf[row_offset + cx] = color_idx
                                cx += 1

                            cy += 1

            i += 1

    def draw_quad(self, vertices, indices, color_idx: int):
        self._draw_quad_internal(vertices, indices, len(indices), int(color_idx))

    @micropython.viper
    def _draw_quad_internal(self, vertices, indices, num_ind: int, color_idx: int):
        width = int(self.width)
        height = int(self.height)
        buf = ptr8(self.buf)
        
        # Signed 32-bit access so negative coordinates don't wrap around
        v = ptr32(vertices)
        ind = ptr16(indices)        
        t = 0

        while t < num_ind:
            i0 = ind[t]
            i1 = ind[t + 1]
            i3 = ind[t + 2]
            i2 = ind[t + 3]

            x0 = v[i0 * 2]
            y0 = v[i0 * 2 + 1]
            x1 = v[i1 * 2]
            y1 = v[i1 * 2 + 1]
            x2 = v[i2 * 2]
            y2 = v[i2 * 2 + 1]
            x3 = v[i3 * 2]
            y3 = v[i3 * 2 + 1]

            # Bounding box calculation
            min_x = x0 if x0 < x1 else x1
            max_x = x0 if x0 > x1 else x1

            if x3 < min_x:
                min_x = x3

            if x3 > max_x:
                max_x = x3

            if x2 < min_x:
                min_x = x2

            if x2 > max_x:
                max_x = x2

            min_y = y0 if y0 < y1 else y1
            max_y = y0 if y0 > y1 else y1

            if y3 < min_y:
                min_y = y3

            if y3 > max_y:
                max_y = y3

            if y2 < min_y:
                min_y = y2

            if y2 > max_y:
                max_y = y2

            # Viewport culling
            if max_x < 0 or min_x >= width or max_y < 0 or min_y >= height:
                t += 4
                continue

            # Clip to screen
            if min_x < 0:
                min_x = 0

            if max_x >= width:
                max_x = width - 1

            if min_y < 0:
                min_y = 0

            if max_y >= height:
                max_y = height - 1

            if min_x <= max_x and min_y <= max_y:
                y = min_y

                while y <= max_y:
                    x = min_x
                    row_offset = y * width

                    while x <= max_x:
                        e0 = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0)
                        e1 = (x3 - x1) * (y - y1) - (y3 - y1) * (x - x1)
                        e2 = (x2 - x3) * (y - y3) - (y2 - y3) * (x - x3)
                        e3 = (x0 - x2) * (y - y2) - (y0 - y2) * (x - x2)

                        if (e0 >= 0 and e1 >= 0 and e2 >= 0 and e3 >= 0) or (e0 <= 0 and e1 <= 0 and e2 <= 0 and e3 <= 0):
                            buf[row_offset + x] = color_idx

                        x += 1

                    y += 1

            t += 4


_fai = _FramebufferAccessInterface()

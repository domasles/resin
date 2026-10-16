import micropython
import resin_hw


class _FramebufferAccessInterface:
    def __init__(self):
        self.width = resin_hw.WIDTH
        self.height = resin_hw.HEIGHT

    @property
    def buf(self):
        return resin_hw.framebuffer()

    def draw_rect(self, x: int, y: int, w: int, h: int, color_idx: int):
        buf = self.buf
        fb_w = self.width
        fb_h = self.height
        
        self._render_rect(buf, fb_w, fb_h, x, y, w, h, color_idx)

    @micropython.viper
    def _render_rect(self, buf, fb_w: int, fb_h: int, x: int, y: int, w: int, h: int, color_idx: int):
        buf_ptr = ptr8(buf)
        
        if x < 0:
            w += x
            x = 0

        if y < 0:
            h += y
            y = 0

        if x + w > fb_w:
            w = fb_w - x

        if y + h > fb_h:
            h = fb_h - y

        if w <= 0 or h <= 0:
            return

        col = int(color_idx)

        for ry in range(y, y + h):
            row_start = ry * fb_w + x

            for rx in range(w):
                buf_ptr[row_start + rx] = col


_fai = _FramebufferAccessInterface()


class Rect:
    def __init__(self, x: int, y: int, w: int, h: int, color: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self):
        _fai.draw_rect(int(self.x), int(self.y), int(self.w), int(self.h), int(self.color))

from ..utils.setting import Setting


class Config:
    bg_color = Setting(0, lambda v: v in range(16))


config = Config()

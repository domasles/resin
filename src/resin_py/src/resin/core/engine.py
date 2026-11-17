import resin_hw

from resin.core.config import config
from resin.core.logger import logger
from resin.core.scene import Scene


class Engine:
    """Framework-owned frame pipeline."""

    def __init__(self):
        """Initializes engine."""

        self.scene = None
        self.quit_flag = False

    def set_scene(self, scene: Scene) -> None:
        """Sets the active scene."""
        self.scene = scene

    def quit(self) -> None:
        """Quits the game."""
        self.quit_flag = True

    def run_frame(self, dt) -> None:
        """Runs one frame - owns frame timing, scene updates, rendering and presentation."""

        if self.quit_flag:
            return

        resin_hw.clear_screen(config.bg_color)

        if self.scene is not None:
            if self.scene.initialized:
                try:
                    self.scene.update(dt)

                except Exception as e:
                    logger.log(f"Runtime error in scene update: {e}")
                    self.scene = None 

        resin_hw.present()


engine = Engine()

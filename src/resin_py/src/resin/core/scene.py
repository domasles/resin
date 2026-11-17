from resin.core.logger import logger


class Scene:
    """Base scene that games branch off of."""

    def __init__(self):
        self.initialized = False

        try:
            self.setup()

        except Exception as e:
            logger.log(f"Start error: {e}")

        self.initialized = True

    def setup(self):
        """Runs before the first frame."""
        pass

    def update(self, dt):
        """Runs on every frame."""
        pass

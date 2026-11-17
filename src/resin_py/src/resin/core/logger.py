import builtins
import time

from micropython import const


class LogLevel:
    DEBUG = const(10)
    INFO = const(20)
    WARNING = const(30)
    ERROR = const(40)
    CRITICAL = const(50)


_LEVEL_NAMES = {
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL"
}


class Logger:
    def __init__(self, level: LogLevel = LogLevel.INFO):
        self.level = level
        self._log_buffer = []
        self._counter = 0

        self._orig_print = builtins.print
        builtins.print = self._hooked_print

    def _hooked_print(self, *args, **kwargs):
        msg = " ".join(str(arg) for arg in args)
        self._add_entry(LogLevel.INFO, msg)

    def _add_entry(self, level, msg):
        self._counter += 1
        self._log_buffer.append((self._counter, level, msg))

        if len(self._log_buffer) > 20:
            self._log_buffer.pop(0)

    def log(self, msg: str, level: LogLevel = LogLevel.INFO) -> None:
        if level >= self.level:
            self._add_entry(level, msg)

    def watch(self) -> None:
        try:
            for _, level, msg in self._log_buffer:
                if level >= self.level:
                    name = _LEVEL_NAMES.get(level, "INFO")
                    self._orig_print(f"[{name}] {msg}")

            last_id = self._log_buffer[-1][0] if self._log_buffer else 0

            while True:
                for item_id, level, msg in self._log_buffer:
                    if item_id > last_id:
                        if level >= self.level:
                            name = _LEVEL_NAMES.get(level, "INFO")
                            self._orig_print(f"[{name}] {msg}")

                        last_id = item_id

                time.sleep(0.05)

        except KeyboardInterrupt:
            return


logger = Logger()

import resin, resin_hw
import _thread
import time

FRAME_TIME_SECONDS = 1.0 / 60.0

def loop():
    last_frame_ms = time.ticks_ms()

    while True:
        now = time.ticks_ms()
        dt = (now - last_frame_ms) / 1000.0
        last_frame_ms = now

        try:
            resin.hardware.input.update()
            resin.engine.run_frame(dt)

        except Exception as e:
            resin.logger.log(f"Loop error: {e}")

        elapsed = (time.ticks_ms() - last_frame_ms) / 1000.0
        sleep_time = FRAME_TIME_SECONDS - elapsed

        if sleep_time > 0:
            time.sleep_ms(max(1, int(sleep_time * 1000)))

def start():
    try:
        resin_hw.init()
        _thread.start_new_thread(loop, ())

    except Exception as e:
        resin.logger.log(f"Failed to start thread: {e}")

if __name__ == "__main__":
    start()

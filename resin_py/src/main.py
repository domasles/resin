import resin, resin_hw
import _thread
import time

logs = []

def log(msg):
    global logs
    logs.append(msg)

    if len(logs) > 20:
        logs.pop(0)

def loop():
    frame_delay_ms = 16

    while True:
        start_time = time.ticks_ms()

        try:
            resin_hw.clear_screen(0)
            resin.hardware.input.update()
            # Current loaded scene's update() goes here
            resin_hw.present()

        except Exception as e:
            log(f"Loop error: {e}")

        elapsed = time.ticks_diff(time.ticks_ms(), start_time)
        sleep_time = max(1, frame_delay_ms - elapsed)

        time.sleep_ms(sleep_time)

def start():
    try:
        resin_hw.init()
        _thread.start_new_thread(loop, ())

    except Exception as e:
        log(f"Failed to start thread: {e}")

if __name__ == "__main__":
    start()

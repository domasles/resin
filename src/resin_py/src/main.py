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
    TARGET_FRAME_MS = 1000 / 60
    
    while True:
        start_time = time.ticks_ms()

        try:
            resin_hw.clear_screen(resin.config.bg_color)
            resin.hardware.input.update()
            main()
            resin_hw.present()

        except Exception as e:
            log(f"Loop error: {e}")

        elapsed = time.ticks_diff(time.ticks_ms(), start_time)
        sleep_time = int(TARGET_FRAME_MS - elapsed)

        if sleep_time > 0:
            time.sleep_ms(sleep_time)

def start():
    try:
        resin_hw.init()
        _thread.start_new_thread(loop, ())

    except Exception as e:
        log(f"Failed to start thread: {e}")

if __name__ == "__main__":
    start()

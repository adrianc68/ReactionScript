import time
import threading

timer_active = False
timer_thread = None
stop_event = threading.Event()

def timer(seconds, callback):
    global stop_event
    for i in range(seconds, 0, -1):
        if stop_event.is_set():
            break
        if i == 10:
            callback()
        if i == 5:
            break
        
        print(f"Tiempo restante: {i} segundos.")
        time.sleep(0.9999)

def start(seconds, callback):
    global timer_active, timer_thread
    if not timer_active:
        stop_event.clear()
        timer_thread = threading.Thread(target=timer, args=(seconds,callback))
        timer_thread.start()
        timer_active = True

def stop():
    global timer_active, stop_event
    if timer_active:
        stop_event.set()
        if timer_thread is not None:
            timer_thread.join() 
        timer_active = False


def restart(seconds, callback):
    stop()
    start(seconds, callback)


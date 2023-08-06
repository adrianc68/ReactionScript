import time

cronometer_active = False
time_list = []

started_time = 0

def start_cronometer():
    global started_time, cronometer_active
    cronometer_active = True
    started_time = time.time()

def stop_cronometer():
    global end_time, cronometer_active
    cronometer_active = False
    end_time = time.time()
    time_elapsed = end_time - started_time
    reset_cronometer()
    return time_elapsed

def reset_cronometer():
    global cronometer_active, started_time
    cronometer_active = False
    started_time = 0    

def restart_cronometer():
    global cronometer_active, time_list, started_time
    
    if cronometer_active:
        time_elapsed = stop_cronometer()
        time_list.append("{:.2f}".format(time_elapsed))
        print(f"Time elapsed: {time_elapsed} seconds")
        print(time_list, "\n")
        restart_cronometer()
    else:
        start_cronometer()


 

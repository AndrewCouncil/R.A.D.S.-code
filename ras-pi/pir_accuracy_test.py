from gpiozero import MotionSensor
from datetime import datetime
import time

pir = MotionSensor(18)

t0 = time.time()
total_seconds = 2*60*60

start_now = datetime.now()
file_name = "logs/accuracy_log_" + start_now.strftime("%m.%d.%y_%H:%M:%S") + ".txt"

while (time.time() - t0) < total_seconds:
    pir.wait_for_motion()
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    message = "Motion detected at  " + current_time
    print(message)
    f = open(file_name, "a")
    f.write(message + "\n")
    f.close()

    time.sleep(2*60)
from gpiozero import MotionSensor
from datetime import datetime
from collections import deque
import time

pir = MotionSensor(18)

start_now = datetime.now()
file_name = "logs/accuracy_log_" + start_now.strftime("%m.%d.%y_%H:%M:%S") + ".txt"

PROGRAM_HZ = 100 #update speed of program in ms
DETECTION_COUNT_THRESHOLD = 40
SENSE_DELAY_SECS = 120
RECORD_DURATION_SECS = 60

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

# Generate queue
queue = deque([False] * (RECORD_DURATION_SECS/(PROGRAM_HZ/1000))) 



t0 = time.time()
total_seconds = 2*60*60
last_person_present = False
detection_count = 0
while (time.time() - t0) < total_seconds:
    # Add element to end of fixed length list
    headval = queue.popleft()
    detection_count -= (int) (headval)
    tailval = pir.motion_detected
    detection_count += (int) (tailval)
    queue.append(tailval)

    person_present = detection_count > DETECTION_COUNT_THRESHOLD
    if last_person_present != person_present:
        now = datetime.now()
        message = "Person present now {}  ".format(person_present) + now.strftime("%H:%M:%S")
        print(message)
        f = open(file_name, "a")
        f.write(message + "\n")
        f.close()

    
    last_person_present = person_present
    time.sleep(PROGRAM_HZ/1000)  
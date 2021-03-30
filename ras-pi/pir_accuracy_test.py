from gpiozero import MotionSensor
from datetime import datetime
from collections import deque
import time

pir = MotionSensor(18)

start_now = datetime.now()
file_name = "logs/accuracy_log_" + start_now.strftime("%m.%d.%y_%H:%M:%S") + ".txt"

PROGRAM_HZ = 100 #update speed of program in ms
SENSE_DELAY_SECS = 120
RECORD_DURATION_SECS = 240
LIST_SIZE =  (int) ((float)(RECORD_DURATION_SECS)/ (float)((float)(PROGRAM_HZ)/1000.0))
DETECTION_COUNT_THRESHOLD = (int)(LIST_SIZE*0.6)

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

# Generate queue
queue = deque([False] * (LIST_SIZE)) 

print("LIST SIZE IS: {}".format(LIST_SIZE))
print("DETECTION THRESHOLD IS: {}".format(DETECTION_COUNT_THRESHOLD))

t0 = time.time()
total_seconds = 2*60*60
last_person_present = False
detection_count = 0
detected_duration = 0.0
while (time.time() - t0) < total_seconds:
    # Add element to end of fixed length list
    headval = queue.popleft()
    detection_count -= (int) (headval)
    tailval = pir.motion_detected
    detection_count += (int) (tailval)
    queue.append(tailval)
    
    person_present = (detection_count > DETECTION_COUNT_THRESHOLD)
    # person_present = False
    # if something_detected:
    #     detected_duration += (float)((float)(PROGRAM_HZ)/1000.0)
    #     if detected_duration > SENSE_DELAY_SECS:
    #         person_present = True
    # else:
    #     detected_duration = 0

    # if person_present:
    #     print(detection_count)
    if last_person_present != person_present:
        print(detection_count)
        print(detected_duration)
        now = datetime.now()
        message = "Person present now {}  ".format(person_present) + now.strftime("%H:%M:%S")
        print(message)
        f = open(file_name, "a")
        f.write(message + "\n")
        f.close()

    print("time testing")
    last_person_present = person_present
    time.sleep((float)((float)(PROGRAM_HZ)/1000.0))  
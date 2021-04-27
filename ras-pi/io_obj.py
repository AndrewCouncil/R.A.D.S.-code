from gpiozero import RGBLED, MotionSensor
from colorzero import Color
from collections import deque
import socket

class RADSInputOutput:
    # PINS
    PIR_PIN = 18
    RED_PIN = 16
    BLUE_PIN = 21
    GREEN_PIN = 20

    PROGRAM_HZ = 30 #update speed of program
    SENSE_DELAY_SECS = 120 #Seconds to delay after sensing before going inactive
    RECORD_DURATION_SECS = 240 #time to store data from pir to average
    QUEUE_SIZE =  (int) ((float)(RECORD_DURATION_SECS)/ (float)((float)(PROGRAM_HZ)/1000.0))
    DETECTION_COUNT_THRESHOLD = (int)(QUEUE_SIZE*0.1)
    
    def __init__(self):
        self.ROOM_NUM = (int) (socket.gethostname()[-1:]) - 1
        self.rgb_led = RGBLED(self.RED_PIN, self.BLUE_PIN, self.GREEN_PIN)
        self.rgb_led.off()
        self.pir_sensor = MotionSensor(self.PIR_PIN)
        #URLs for data
        self.ROOT_URL = 'http://www.roomavailable.info'
        self.FALSE_ROOM_URL = self.ROOT_URL + "/test?r={}&f=0".format(self.ROOM_NUM)
        self.TRUE_ROOM_URL  = self.ROOT_URL + "/test?r={}&f=1".format(self.ROOM_NUM)
        
        # set up fi-lo queue for pir data
        self.queue = deque([False] * (self.LIST_SIZE)) 

        

from gpiozero import RGBLED, MotionSensor
from colorzero import Color
import socket

class RADSInputOutput:
    # PINS
    PIR_PIN = 18
    RED_PIN = 16
    BLUE_PIN = 21
    GREEN_PIN = 20

    SENSE_DELAY_SECS = 120 #Seconds to delay after sensing before going inactive
    DISTANCE_RESET_SECS = 1 * 3600 #Seconds of no pir activity that will reset distance sensor
    DEFAULT_MAXIMUM_METERS = 1 #Distance in meters
    PROGRAM_HZ = 30 #update speed of program

    
    def __init__(self):
        self.ROOM_NUM = (int) (socket.gethostname()[-1:])
        self.rgb_led = RGBLED(self.RED_PIN, self.BLUE_PIN, self.GREEN_PIN)
        self.rgb_led.off()
        self.pir_sensor = MotionSensor(self.PIR_PIN)
        #URLs for data
        self.ROOT_URL = 'http://54.147.192.125'
        self.FALSE_ROOM_URL = self.ROOT_URL + "/roomdata?r={}&f=0".format(self.ROOM_NUM)
        self.TRUE_ROOM_URL  = self.ROOT_URL + "/roomdata?r={}&f=1".format(self.ROOM_NUM)

        
from gpiozero import MotionSensor
from time import sleep

pir = MotionSensor(18)
while True:
    print(pir.motion_detected)
    sleep(.5)
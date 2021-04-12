from gpiozero import RGBLED
from colorzero import Color
from time import sleep
import os

RED_PIN = 16
BLUE_PIN = 21
GREEN_PIN = 20

rgb_led = RGBLED(RED_PIN, BLUE_PIN, GREEN_PIN)
rgb_led.on()
rgb_led.color = Color("green")
sleep(5)


try:
    os.system("git pull /home/pi/RADS-code")
except:
    rgb_led.color = Color("red")
    raise RuntimeError("Pulling of updated program failed!")


print("Starting rgb")
os.system("sudo python rgb_test.py &")
print("started already")
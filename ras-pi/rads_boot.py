from gpiozero import RGBLED
from colorzero import Color
from time import sleep
from rgb_test import test_rgb
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
    sleep(5)
    raise RuntimeError("Pulling of updated program failed!")


print("Starting rgb")
test_rgb()
print("started already")
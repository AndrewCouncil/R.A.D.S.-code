from gpiozero import RGBLED
from colorzero import Color
from time import sleep
from rgb_test import test_rgb
from gpio_obj import RADSInputOutput
import os


rads = RADSInputOutput()
rads.rgb_led.color = Color("green")
sleep(5)


try:
    os.system("git pull /home/pi/RADS-code")
except:
    rads.rgb_led.color = Color("red")
    sleep(5)
    raise RuntimeError("Pulling of updated program failed!")


print("Starting rgb")
test_rgb(rads)
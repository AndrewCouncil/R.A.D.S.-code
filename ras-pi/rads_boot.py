from gpiozero import RGBLED
from colorzero import Color
from time import sleep
from rgb_test import test_rgb
from gpio_obj import RADSInputOutput
import os, git

# TEST COMMENT TO TEST PULL OF GITHUB

rads = RADSInputOutput()
rads.rgb_led.color = Color("green")
sleep(5)

g = git.cmd.Git("/home/pi/RADS-code")
try:
    g.pull()
except:
    rads.rgb_led.color = Color("red")
    sleep(5)
    raise RuntimeError("Pulling of updated program failed!")


print("Starting rgb")
test_rgb(rads)
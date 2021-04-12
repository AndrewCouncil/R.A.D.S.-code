from colorzero import Color
from time import sleep
from rgb_test import test_rgb
from gpio_obj import RADSInputOutput
from network_tools import network_wait
import git

# init io object and show green for 5 seconds on boot
rads = RADSInputOutput()
rads.rgb_led.color = Color("green")
sleep(5)

# network_wait(rads)

# Pull updated code from github REQUIRES REBOOT TO CHANGE STUFF
g = git.cmd.Git("/home/pi/RADS-code")
try:
    g.pull()
except:
    rads.rgb_led.color = Color("red")
    sleep(5)
    raise RuntimeError("Pulling of updated program failed!")


print("Starting rgb")
test_rgb(rads)
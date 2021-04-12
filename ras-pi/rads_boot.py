from gpiozero import RGBLED
from colorzero import Color
import requests, os, sys

try:
    os.system("git pull /home/pi/RADS-code")
except:
    raise RuntimeError("Pulling of updated program failed!")


print("Starting rgb")
os.system("sudo python rgb_test.py &")
print("started already")
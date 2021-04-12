from gpiozero import RGBLED
from colorzero import Color
from time import sleep

RED_PIN = 16
BLUE_PIN = 21
GREEN_PIN = 20

rgb_led = RGBLED(RED_PIN, BLUE_PIN, GREEN_PIN)

rgb_led.on()
while True:
	rgb_led.color = Color("red")
	sleep(1)
	rgb_led.color = Color("green")
        sleep(1)
	rgb_led.color = Color("blue")
        sleep(1)

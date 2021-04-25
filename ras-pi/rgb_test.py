from gpiozero import RGBLED
from colorzero import Color
from time import sleep
from gpio_obj import RADSInputOutput


def test_rgb(rads):
	rads.rgb_led.on()
	while True:
		rads.rgb_led.color = Color("orange")
		sleep(1)
		# rads.rgb_led.color = Color("purple")
		# sleep(1)
		# rads.rgb_led.color = Color("blue")
		# sleep(1)

if __name__ == "__main__":
	rads_main = RADSInputOutput()
	test_rgb(rads_main)
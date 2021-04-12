from gpiozero import RGBLED
from colorzero import Color
from time import sleep
from gpio_obj import RADSInputOutput

# TEST COMMENT TO TEST PULL OF GITHUB

def test_rgb(rads):
	rads.rgb_led.on()
	while True:
		rads.rgb_led.color = Color("red")
		sleep(1)
		rads.rgb_led.color = Color("green")
		sleep(1)
		rads.rgb_led.color = Color("blue")
		sleep(1)

if __name__ == "__main__":
	rads_main = RADSInputOutput()
	test_rgb(rads_main)
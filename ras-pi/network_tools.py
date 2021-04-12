import requests
from gpiozero import RGBLED
from colorzero import Color
from time import sleep


# Waits for network connection and valid http requests from the ROOT_URL
def network_wait(rgb_led, PROGRAM_HZ):
    print("network error!")
    while True:
        # Check if pinging google works
        ping_result = requests.get("http://google.com")
        # If it worked, test http request
        if ping_result.status_code < 300:
            # Try the request, and if it works and has a good status code, exit the function
            try:
                r = requests.get(ROOT_URL)
                if r.status_code < 300:
                    print("\nnetwork online!")
                    return
                else:
                    # If status code is bad print and continue
                    print("bad status code...")
            except:
                # If request errors print and continue
                print("request not received...")
        # If it didn't, print and check again
        else:
            print("ping to google not working, likely no internet connection...")
        
        # Set LED to yellow and wait to match PROGRAM_HZ
        rgb_led.color = Color('yellow')
        sleep(PROGRAM_HZ/1000)
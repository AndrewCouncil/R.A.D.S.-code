from requests.api import request
from gpiozero import RGBLED, Button, DistanceSensor, LED
from colorzero import Color
from time import sleep
import requests, os, sys

ROOM_NUM = 1

SENSE_DELAY_SECS = 120 #Seconds to delay after sensing before going inactive
DISTANCE_RESET_SECS = 1 * 3600 #Seconds of no pir activity that will reset distance sensor
DEFAULT_MAXIMUM_METERS = 1 #Distance in meters
PROGRAM_HZ = 30 #update speed of program

# PINS
PIR_PIN = 18
RED_PIN = 16
BLUE_PIN = 20
GREEN_PIN = 21

#URLs for data
ROOT_URL = 'http://54.147.192.125'
if "-local" in sys.argv:
    ROOT_URL = 'http://localhost:5000'
FALSE_ROOM_URL = "/roomdata?r={}&f=0".format(ROOM_NUM)
TRUE_ROOM_URL  = "/roomdata?r={}&f=1".format(ROOM_NUM)

# Sensor and output setup
pir_sensor = Button(PIR_PIN, True)
rgb_led = RGBLED(RED_PIN, BLUE_PIN, GREEN_PIN)
rgb_led.off()

# Waits for network connection and valid http requests from the ROOT_URL
def network_wait():
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

# Sent a http request to the given url, checking for any network errors
def send_http(url):
    # Check pinging google, if any issues go to network_wait
    ping_result = requests.get("http://google.com")
    if ping_result.status_code >= 300: network_wait()
    # perform http request using requests, if any errors go to network wait and try again once it exits
    print("sending url: " + url)
    try:
        r = requests.get(url)
        if r.status_code >= 300: 
            network_wait()
            r = requests.get(url)
    except:
        network_wait()
        r = requests.get(url)
    print("url sent!\n")
    

# VARIABLE BOUNDING
time_total = 0
person_detected = False
person_present = False
person_was_present = False
jam_pressed = False
jam_was_pressed = False
jam_on = False
jam_was_on = False
pir_not_detected_time = 0
max_meters = DEFAULT_MAXIMUM_METERS

def main_work():
    # set vars global
    global time_total
    global person_detected
    global person_present
    global person_was_present
    global pir_not_detected_time
    # -----------------PERSON DETECTION-----------------
    # If pir or distance sensor tripped, person_detected is True
    person_detected = False
    if not pir_sensor.is_pressed:
        person_detected = True
        pir_not_detected_time = 0
    else:
        # If pir off for more than DISTANCE_RESET_SECS, reset the maximum distance for the distance sensor
        if pir_not_detected_time > DISTANCE_RESET_SECS*1000:
            # max_meters = distance_sensor.distance()
            pir_not_detected_time = 0
        else:
            pir_not_detected_time += PROGRAM_HZ


    # If a person is detected, set person_present to True
    if person_detected:
        person_present = True
        time_total = 0
    # If a person is not detected, wait until SENSE_DELAY_SECS and then set person_present to False
    else:
        if time_total > SENSE_DELAY_SECS * 1000:
            person_present = False
        else:
            time_total += PROGRAM_HZ

    # If person_present is different than person_was_present, the status has changed
    # Send a HTTP request in this case
    if person_present != person_was_present:
        print("person change detected!")
        request_url = ROOT_URL
        if person_present:
            print("person on now")
            request_url += TRUE_ROOM_URL
        else:
            print("person off now")
            request_url += FALSE_ROOM_URL
        
        send_http(request_url)

    person_was_present = person_present


    # Set LED to green and sleep for PROGRAM_HZ time
    rgb_led.on()
    rgb_led.color = Color('green')
    sleep(PROGRAM_HZ/1000)

def testing():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print(pir_sensor.is_pressed)

    rgb_led.color = Color('yellow')
    rgb_led.on()
    sleep(500)
    

# Runs the code in normal mode if testing flag is present, otherwise sets led to red if any errors
if sys.argv[1] == "-testing":
    while True: testing()

send_http(ROOT_URL + FALSE_ROOM_URL)
if sys.argv[1] == "-v":
    print("starting")
    while True: main_work()
else:
    while True:
        try:
            main_work()
        except:
            rgb_led.color = Color('red')
            print("Error has ocurred in main loop!")

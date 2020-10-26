from requests.api import request
from gpiozero import RGBLED, Button, DistanceSensor, LED
from colorzero import Color
from time import sleep
import requests, os

SENSE_DELAY_SECS = 120 #Seconds to delay after sensing before going inactive
MAXIMUM_DISTANCE = 1 #Distance in meters
PROGRAM_HZ = 30 #update speed of program
JAM_BUTTON_PIN = 7
JAM_LED_PIN = 9
PIR_PIN = 4
DISTANCE_ECHO_PIN = 18
DISTANCE_TRIGGER_PIN = 17
RED_PIN = 2
BLUE_PIN = 3
GREEN_PIN = 4
ROOT_URL = 'https://test.com'
FALSE_ROOM_URL = "idkyet"
TRUE_ROOM_URL = "idkyet"
FALSE_JAM_URL = "idkyet"
TRUE_JAM_URL = "idkyet"

time_total = 0
person_detected = False
person_present = False
person_was_present = False
jam_pressed = False
jam_was_pressed = False
jam_on = False
jam_was_on = False

pir_sensor = Button(PIR_PIN, True)
distance_sensor = DistanceSensor(echo=DISTANCE_ECHO_PIN, trigger=DISTANCE_TRIGGER_PIN)
rgb_led = RGBLED(RED_PIN, BLUE_PIN, GREEN_PIN)
rgb_led.off()
jam_led = LED(JAM_LED_PIN)
jam_led.off()
jam_button = Button(JAM_BUTTON_PIN, True)

def network_error():
    print("network error!")
    while True:
        ping_result = os.popen('ping google.com').read()
        if "Received = 4" in ping_result:
            r = requests.get(ROOT_URL)
            if r.status_code < 300:
                print("\nnetwork back online!")
                return
        
        rgb_led.color = Color('yellow')
        sleep(PROGRAM_HZ/1000)

def send_http(url):
    ping_result = os.popen('ping google.com').read()
    if "Received = 4" not in ping_result: network_error()

    r = requests.get(url)
    if r.status_code >= 300: 
        network_error()
        r = requests.get(url)

while True:
    rgb_led.color = Color('green')

    # PERSON DETECTION
    person_detected = False
    if pir_sensor.is_pressed():
        person_detected = True
    if distance_sensor.distance() <= MAXIMUM_DISTANCE:
        person_detected = True

    if person_detected:
        person_present = True
        time_total = 0
    else:
        time_total += PROGRAM_HZ
        if time_total > SENSE_DELAY_SECS * 1000:
            person_present = False

    if person_present != person_was_present:
        print("change detected!")
        request_url = ROOT_URL
        if person_present:
            request_url += TRUE_ROOM_URL
        else:
            request_url += FALSE_ROOM_URL
        
        send_http(request_url)

    person_was_present = person_present

    # JAM BUTTON
    if not person_present:
        jam_on = False
    else:
        jam_pressed = jam_button.is_pressed()
        if jam_pressed and not jam_was_pressed:
            jam_on = not jam_on
        jam_was_pressed = jam_pressed

    if jam_on != jam_was_on:
        jam_led.toggle()
        request_url = ROOT_URL
        if jam_on:
            request_url += TRUE_JAM_URL
        else:
            request_url += FALSE_JAM_URL
        
        send_http(request_url)

    jam_was_on = jam_on

    sleep(PROGRAM_HZ/1000)


    

print("I run now")
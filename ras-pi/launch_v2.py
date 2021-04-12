from colorzero import Color
from time import sleep
from gpio_obj import RADSInputOutput
from network_tools import send_http
import sys


# VARIABLE BOUNDING
time_total = 0
person_detected = False
person_present = False
person_was_present = False
pir_not_detected_time = 0

def main_work(rads):
    # set vars global
    global time_total
    global person_detected
    global person_present
    global person_was_present
    global pir_not_detected_time
    # -----------------PERSON DETECTION-----------------
    # If pir or distance sensor tripped, person_detected is True
    person_detected = False
    if not rads.pir_sensor.motion_detected:
        person_detected = True
        pir_not_detected_time = 0
    else:
        # If pir off for more than DISTANCE_RESET_SECS, reset the maximum distance for the distance sensor
        if pir_not_detected_time > rads.DISTANCE_RESET_SECS*1000:
            # max_meters = distance_sensor.distance()
            pir_not_detected_time = 0
        else:
            pir_not_detected_time += rads.PROGRAM_HZ


    # If a person is detected, set person_present to True
    if person_detected:
        person_present = True
        time_total = 0
    # If a person is not detected, wait until SENSE_DELAY_SECS and then set person_present to False
    else:
        if time_total > rads.SENSE_DELAY_SECS * 1000:
            person_present = False
        else:
            time_total += rads.PROGRAM_HZ

    # If person_present is different than person_was_present, the status has changed
    # Send a HTTP request in this case
    if person_present != person_was_present:
        print("person change detected!")
        if person_present:
            print("person on now")
            request_url = rads.TRUE_ROOM_URL
        else:
            print("person off now")
            request_url = rads.FALSE_ROOM_URL
        
        send_http(request_url)

    person_was_present = person_present


    # Set LED to green and sleep for PROGRAM_HZ time
    rads.rgb_led.on()
    rads.rgb_led.color = Color('green')
    sleep(rads.PROGRAM_HZ/1000)

def testing(rads):
    # os.system('cls' if os.name == 'nt' else 'clear')
    print(rads.pir_sensor.motion_detected)

    rads.rgb_led.color = Color('yellow')
    rads.rgb_led.on()
    sleep(0.5)
    

# Runs the code in normal mode if testing flag is present, otherwise sets led to red if any errors
def run(rads):
    if sys.argv[1] == "-testing":
        while True: testing(rads)
    
    send_http(rads.FALSE_ROOM_URL)
    if sys.argv[1] == "-v":
        print("starting")
        while True: main_work(rads)
    else:
        while True:
            try:
                main_work(rads)
            except:
                rads.rgb_led.color = Color('red')
                print("Error has ocurred in main loop!")


if __name__ == "__main__":
    rads_main = RADSInputOutput()
    run(rads_main)
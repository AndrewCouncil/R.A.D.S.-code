import requests
from colorzero import Color
from time import sleep


# Waits for network connection and valid http requests from the ROOT_URL
def network_wait(rads):
    print("network error!")
    while True:
        # Check if pinging google works
        ping_result = requests.get("http://google.com")
        # If it worked, test http request
        if ping_result.status_code < 300:
            # Try the request, and if it works and has a good status code, exit the function
            try:
                r = requests.get(rads.ROOT_URL)
                if r.status_code < 300:
                    print("\nnetwork online!")
                    return
                else:
                    # If status code is bad print and continue
                    print("bad status code, rads site inaccesible...")
            except:
                # If request errors print and continue
                print("request not received...")
        # If it didn't, print and check again
        else:
            print("ping to google not working, likely no internet connection...")
        
        # Set LED to yellow and wait to match PROGRAM_HZ
        rads.rgb_led.color = Color('yellow')
        sleep(rads.PROGRAM_HZ/1000)


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
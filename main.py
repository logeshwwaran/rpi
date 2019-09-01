import sys
from auth import MiBand3
from cursesmenu import *
from cursesmenu.items import *
import time
import os
import time
import requests
import math
import random
from datetime import datetime


MAC_ADDR= 'D9:C6:8D:E1:FF:3A'
def l(x):
    print 'Realtime heart BPM:', x
    
    payload = build_payload(x)
    band.stop_realtime()
    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")
    time.sleep(20)
    band.start_raw_data_realtime(heart_measure_callback=l)
band = MiBand3(MAC_ADDR, debug=True)
band.setSecurityLevel(level = "medium")

band.authenticate()
TOKEN = "BBFF-9f0ooUnFzfnJ6R8aGsJzdL7Wtrg6MG"  # Put your TOKEN here
DEVICE_LABEL = "machine"  # Put your device label here 


def build_payload(value_1):
    variable_1='heartrate'
    variable_2='time'
    now = datetime.now()
    value_2= now.strftime("%H:%M:%S")
    payload = {variable_1:value_1 ,
                variable_2:value_2}

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


band.start_raw_data_realtime(heart_measure_callback=l)

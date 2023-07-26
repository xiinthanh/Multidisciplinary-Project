import sys
import random
import time
import requests
import serial.tools.list_ports
from random import randint
from Adafruit_IO import MQTTClient

from simple_ai import mask_detector

AIO_USERNAME = "DiscreteGroup"
# AIO_KEY is saved in aio_key.txt
AIO_KEY = open("aio_key.txt", "r").read()

# Feeds which will be subscribed (we receive data from these feeds)
AIO_FEED_ID = ["password", "confirm-button", "average-temp-equation"]

# Save the last 3 temperatures for Data Analysis
temperature = [0, 0, 0]

CORRECT_PASSWORD = "123456#"
typed_password = ""
validate_through_password = False

def passwordIsCorrect():
    global typed_password
    if typed_password == CORRECT_PASSWORD:
        return True
    return False

# IoT
def connected(client):
    print("Server connected ...")
    for FEED_ID in AIO_FEED_ID:
        client.subscribe(FEED_ID)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed...")

def disconnected(client):
    print("Disconnected from the server...")
    sys.exit(1)

def openTheDoor():
    '''Open the door for 10s.'''
    client.publish("door-button", 1)
    time.sleep(10)
    client.publish("door-button", 0)

def message(client, feed_id, payload):
    print("Received data: " + payload)
    if feed_id == "average-temp-equation":
        global global_equation
        global_equation = payload
        print("New average temperature equation:", global_equation)

    global typed_password
    if feed_id == "password":
        typed_password += str(payload)

    if feed_id == "confirm-button":
        if passwordIsCorrect():
            global validate_through_password
            validate_through_password = True
        # Reset
        typed_password = ""

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()


# Data Analysis

# Equation for Data Analytic
global_equation = ""

def init_global_equation():
    headers = {}
    aio_url = "	https://io.adafruit.com/api/v2/DiscreteGroup/feeds/average-temp-equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data = x.json()
    global global_equation
    global_equation = data["last_value"]
    print("Get lastest value:", global_equation)

init_global_equation()

def modify_value(x1, x2, x3):
    global global_equation
    result = eval(global_equation)
    return result


# Simple hardware device - Arduino
# If we send "0" to Arduino, it will send back the body temperature.

# ser = serial.Serial(port="COMx", baudrate=115200)
ser = serial.Serial(port="COM5", baudrate=115200)


def sendCommand(cmd):
    ser.write(cmd.encode())

mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")

    # Format: splitData = [ID(1, 2, ...), TAG(T), VALUE].
    
    # The body temperature: splitData[2]
    # Drop temperature[0] and add a new temperature.
    temperature[0] = temperature[1]
    temperature[1] = temperature[2]
    temperature[2] = splitData[2]
    client.publish("body-temperature", temperature[2])
    client.publish("average-temperature", modify_value(temperature[0], temperature[1], temperature[2]))

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end + 1:]

def requestData(cmd):
    sendCommand(cmd)
    time.sleep(1)
    readSerial()

while True:
    requestData("0")

    # Normal temperature range: [36.1, 37.2]
    if 36.1 <= temperature[2] and temperature[2] <= 37.2 and mask_detector():
        openTheDoor()
    elif validate_through_password:
        openTheDoor()
        validate_through_password = False
    
    time.sleep(3)

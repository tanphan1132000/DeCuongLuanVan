print("Hello AIoT")
import sys
from Adafruit_IO import MQTTClient
import time
import port
import serial.tools.list_ports
import read_sensors
import pump_control

AIO_FEED_ID = ["doanktmt.temp"]
AIO_USERNAME = "DoAnBachKhoa"
AIO_KEY = "aio_uUiN12G52bUDlFQejB2zxhzesNUY"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Payload: " + payload)
    # if feed_id == "actuator1":
    #     if payload == "1":
    #         setDevice1(True)
    #     else:
    #         setDevice1(False)


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

portName = port.getPort()
print("Port: " + portName)
if portName != "None":
    ser = serial.Serial(port=portName, baudrate=9600)

while True:
    print("Running...")
    time.sleep(5)
    # image_capture()
    # ai_result = image_detector()
    # client.publish("visiondetection", ai_result)
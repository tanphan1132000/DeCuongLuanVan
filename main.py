print("Hello AIoT")
import sys
from Adafruit_IO import MQTTClient
import time
import port
import serial.tools.list_ports
import read_sensors
import pump_control
import model

AIO_FEED_ID = ["doanktmt.temp", "doanktmt.humi", "doanktmt.pump"]
AIO_USERNAME = "DoAnBachKhoa"
AIO_KEY = "aio_EiYf93DMpKgrI4xdbS9zj36eFIt1"

portName = port.getPort()
print("Port: " + portName)
if portName != "None":
    ser = serial.Serial(port=portName, baudrate=9600)

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
    if feed_id == "doanktmt.temp": print("Temperature: " + payload)
    elif feed_id == "doanktmt.humi": print("Humidity: " + payload)
    elif feed_id == "doanktmt.pump":
        if payload == "1":
            pump_control.setDevice1(True, ser)
            print("Pump: ON")
        else:
            pump_control.setDevice1(False, ser)
            print("Pump: OFF")


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

# while True:
    # value_temp = read_sensors.readTemperature(ser, port.serial_read_data)/10
    # client.publish("doanktmt.temp", value_temp)
    # time.sleep(2)
    # value_humi = read_sensors.readMoisture(ser, port.serial_read_data)/10
    # client.publish("doanktmt.humi", value_humi)
    # time.sleep(2)

model.image_capture()
ai_result = model.image_detector()
    # client.publish("visiondetection", ai_result)
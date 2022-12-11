print("Hello AIoT")
import sys
from Adafruit_IO import MQTTClient
import time
import port
import serial.tools.list_ports
import serial.rs485
import read_sensors
import pump_control
from model import model

AIO_FEED_ID = ["doanktmt.pump"]
AIO_USERNAME = "DoAnBachKhoa"
AIO_KEY = "aio_EiYf93DMpKgrI4xdbS9zj36eFIt1"

count = 1
count_detect = 1
isPumpSignal = False
isPump = False

portName = port.getPort()
print("Port: " + portName)
if portName != "None":
    ser = serial.Serial(port=portName, baudrate=9600)
    ser.rs485_mode = serial.rs485.RS485Settings()

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
    if feed_id == "doanktmt.pump":
        global isPumpSignal, isPump
        isPumpSignal = True
        if payload == "1":
            isPump = True
            print("Pump: ON")
        else:
            isPump = False
            print("Pump: OFF")


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    if count == 50:
        value_temp = read_sensors.readTemperature(ser, port.serial_read_data)/10
        print(f"Temperature: {value_temp}°C")
        client.publish("doanktmt.temp", value_temp)
    # if count == 80:
        value_humi = read_sensors.readMoisture(ser, port.serial_read_data)/10
        print(f"Humidity: {value_humi}%")
        client.publish("doanktmt.humi", value_humi)
        count = 0
    if isPumpSignal:
        if isPump:
            pump_control.setDevice2(True, ser)
        else:
            pump_control.setDevice2(False, ser)
        isPumpSignal = False
    if count_detect == 100:
        print('Detecting...')
        model.image_capture()
        ai_result = model.image_detector()
        client.publish("doanktmt.plantdetection", ai_result)
        count_detect = 0

    count_detect += 1
    count += 1
    time.sleep(0.1)
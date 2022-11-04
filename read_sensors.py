import time

print("Test Sensors")
soil_temperature =[3, 3, 0, 0, 0, 1, 133, 232]
def readTemperature(ser, serial_read_data):
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)

soil_moisture = [3, 3, 0, 1, 0, 1, 212, 40]
def readMoisture(ser, serial_read_data):
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)
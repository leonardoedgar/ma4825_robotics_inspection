#!/usr/bin/python3
from communication.serial_device import SerialDevice
import os


if __name__ == '__main__':
    arduino = SerialDevice(port=os.getenv("SERIAL_DEVICE_PORT"), baud_rate=9600)
    while True:
        try:
            data_to_send = arduino.get_request()
            print("Received arduino data: ", data_to_send)
            data_to_send += 1
            arduino.send_response(data_to_send)
        except KeyboardInterrupt:
            break

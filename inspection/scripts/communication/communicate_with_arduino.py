#!/usr/bin/python3
from communication.serial_device import SerialDevice
import os


if __name__ == '__main__':
    arduino = SerialDevice(port=os.getenv("SERIAL_DEVICE_PORT"), baud_rate=9600)
    data_to_send = 1
    while True:
        try:
            print("Received arduino data: ", arduino.get_request())
            arduino.send_response(data_to_send)
            data_to_send += 1
        except KeyboardInterrupt:
            break

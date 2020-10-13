#!/usr/bin/python3
from exception.exception import HardwareException
import serial
import time


class SerialDevice(object):
    """A class to represent the serial device."""
    def __init__(self, port, baud_rate):
        # type: (str, int) -> None
        """Initialise the class.
        Args:
            port: the port of the serial device
            baud_rate: the baud rate of the serial communication
        """
        self.__serial_device = None
        num_of_attempts, max_num_of_connection_attempts = 0, 5
        while num_of_attempts < max_num_of_connection_attempts:
            try:
                self.__serial_device = serial.Serial(port=port, baudrate=baud_rate, timeout=None)
            except serial.SerialException:
                print("Unable to find serial device in port: %s. Retrying." % port)
                time.sleep(0.2)
                num_of_attempts += 1
            else:
                break
        if self.__serial_device is None:
            raise HardwareException("Failed in finding serial device in port: %s after %d attempts"
                                    % (port, num_of_attempts))

    def get_request(self, num_bytes=1):
        # type: (int) -> int
        """A function to get a request data from the serial device.
        Args:
            num_bytes: number of bytes to read
        """
        return int.from_bytes(self.__serial_device.read(size=num_bytes), byteorder="big")

    def send_response(self, resp):
        # type: (int) -> None
        """A function to send a response data to the serial device.
        Args:
            resp: response data to send
        """
        self.__serial_device.write(str.encode(str(resp)))

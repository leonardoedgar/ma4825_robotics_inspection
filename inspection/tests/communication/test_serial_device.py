#!/usr/bin/python3
from communication.serial_device import SerialDevice
from exception.exception import HardwareException
import pytest


SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600


def get_mocked_serial_device(mocker, port, baud_rate):
    """A function to get a mocked serial device."""
    mocked_serial = mocker.patch("serial.Serial")
    return mocked_serial, SerialDevice(port=port, baud_rate=baud_rate)


def test_success_initialisation(mocker):
    """A function to test that serial device can be initialised."""
    mocked_serial, _ = get_mocked_serial_device(mocker, SERIAL_PORT, BAUD_RATE)
    assert mocked_serial.call_args[1]["port"] == SERIAL_PORT
    assert mocked_serial.call_args[1]["baudrate"] == BAUD_RATE


def test_failed_initialisation(mocker):
    """A function to test that failed initialisation is handled."""
    mocker.patch("serial.Serial", side_effect=HardwareException())
    with pytest.raises(HardwareException):
        SerialDevice(port=SERIAL_PORT, baud_rate=BAUD_RATE)


def test_get_request(mocker):
    """A function to test that serial device can receive request."""
    mocked_serial, serial_device = get_mocked_serial_device(mocker, SERIAL_PORT, BAUD_RATE)
    test_byte = 5
    mocked_serial().read.return_value = bytes([test_byte])
    assert serial_device.get_request() == test_byte


def test_send_response(mocker):
    """A function to test that serial device can send response."""
    mocked_serial, serial_device = get_mocked_serial_device(mocker, SERIAL_PORT, BAUD_RATE)
    test_int = 1
    serial_device.send_response(test_int)
    assert mocked_serial().write.call_args[0][0] == bytes([test_int])

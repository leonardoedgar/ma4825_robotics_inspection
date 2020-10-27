#!/usr/bin/python3
from communication.serial_device import SerialDevice
from hardware.uvc_driver import UVCDriver
from vision.defect_detector import DefectDetector
from exception.exception import HardwareException
from pathlib import Path
import os
import threading
import time
import cv2
import calibration
import yaml


def start_vision_server(serial_device, detector, camera_driver):
    """A function to start the vision server.
    Args:
          serial_device: a serial device to get request from
          detector: a detector class to provide detection service
          camera_driver: a camera driver to grab image for inspection
    """
    # type: (SerialDevice, DefectDetector, UVCDriver)
    while True:
        try:
            request_id = 0
            print("Waiting for detection request from arduino.")
            while request_id != 1:
                request_id = serial_device.get_request()
            print("Received request from arduino: %d" % request_id)
            is_grab_image_success = False
            while not is_grab_image_success:
                try:
                    if detector.is_object_defected(image=camera_driver.capture_image(),
                                                   show_window=True):
                        response_id = 2
                    else:
                        response_id = 3
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                except HardwareException as err:
                    print("Err: %s" % err)
                else:
                    print("Sending response id: %d to arduino" % response_id)
                    serial_device.send_response(resp=response_id)
                    is_grab_image_success = True
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    camera_config_path = os.path.join(Path(calibration.__file__).parent, "config", "intrinsic",
                                      "camera_info.yaml")
    with open(camera_config_path) as camera_config_file:
        camera_config = yaml.load(stream=camera_config_file)
        with open(camera_config["config"]["intrinsic"]) as camera_params_file:
            camera_params = yaml.load(stream=camera_params_file)
    arduino = SerialDevice(port=os.getenv("SERIAL_DEVICE_PORT"), baud_rate=9600)
    uvc_driver = UVCDriver(video_device_id=int(os.getenv("VIDEO_DEVICE_ID")),
                           frame_res=(1280, 960))
    defect_detector = DefectDetector()
    uvc_thread = threading.Thread(target=uvc_driver.start)
    arduino_thread = threading.Thread(target=start_vision_server,
                                      args=(arduino, defect_detector, uvc_driver,))
    uvc_thread.start()
    arduino_thread.start()
    uvc_thread.join()
    arduino_thread.join()
    uvc_driver.release()
    time.sleep(1)

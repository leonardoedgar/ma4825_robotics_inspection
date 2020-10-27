#!/usr/bin/python3
from hardware.uvc_driver import UVCDriver
from vision.defect_detector import DefectDetector
from exception.exception import HardwareException
from pathlib import Path
import cv2
import os
import threading
import time
import yaml
import calibration


def detect_defect():
    """A function to detect defect from an image taken by a camera."""
    while True:
        try:
            detector.is_object_defected(image=uvc_driver.capture_image(), show_window=True)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except HardwareException as err:
            print("Err: %s" % err)
            time.sleep(0.5)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    camera_config_path = os.path.join(Path(calibration.__file__).parent, "config", "intrinsic",
                                      "camera_info.yaml")
    with open(camera_config_path) as camera_config_file:
        camera_config = yaml.load(stream=camera_config_file)
        with open(camera_config["config"]["intrinsic"]) as camera_params_file:
            camera_params = yaml.load(stream=camera_params_file)
    uvc_driver = UVCDriver(
        video_device_id=int(os.getenv("VIDEO_DEVICE_ID")),
        frame_res=(1280, 960))
    detector = DefectDetector(camera_params=camera_params)
    uvc_thread = threading.Thread(target=uvc_driver.start)
    image_processor_thread = threading.Thread(target=detect_defect)
    uvc_thread.start()
    image_processor_thread.start()
    uvc_thread.join()
    image_processor_thread.join()
    uvc_driver.release()
    time.sleep(1)

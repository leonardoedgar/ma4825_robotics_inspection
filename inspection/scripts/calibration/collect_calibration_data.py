#!/usr/bin/python3
from calibration.image_collector import ImageCollector
from hardware.uvc_driver import UVCDriver
import threading
import os
import calibration


def get_user_prompt_to_save_data(data_collector):
    # type: (ImageCollector) -> None
    """A function to a user input"""
    is_collect_more_data = True
    while is_collect_more_data:
        user_input = input("Capture current frame (y/n): ").lower()
        if user_input == "y":
            data_collector.save_image()
        user_input = input("Collect more data (y/n): ").lower()
        while user_input != "y" and user_input != "n":
            print("Invalid input. Only answer the prompt with 'y' or 'n'")
            user_input = input("Collect more data (y/n(: ").lower()
        is_collect_more_data = user_input == "y"


if __name__ == '__main__':
    uvc_driver = UVCDriver(video_device_id=int(os.getenv("VIDEO_DEVICE_ID")), frame_res=(1280, 960))
    image_collector = ImageCollector(
        uvc_driver=uvc_driver,
        dir_to_save=os.path.join(os.path.dirname(calibration.__file__), "data", "original"))
    data_collector_thread = threading.Thread(target=get_user_prompt_to_save_data, args=(image_collector,))
    uvc_streamer_thread = threading.Thread(target=uvc_driver.start)
    data_collector_thread.start()
    uvc_streamer_thread.start()
    data_collector_thread.join()
    uvc_streamer_thread.join()
    uvc_driver.release()

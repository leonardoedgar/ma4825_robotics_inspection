#!/usr/bin/python3
import cv2
import datetime
import os
from hardware.uvc_driver import UVCDriver


class ImageCollector(object):
    """
    A class to represent the image saver.
    """
    def __init__(self, uvc_driver, dir_to_save):
        # type: (UVCDriver, str) -> None
        """Initialise the class.
        Args:
            uvc_driver: the universal video camera device driver.
            dir_to_save: the directory to save the images.
        """
        self.__uvc_driver = uvc_driver
        self.__dir_to_save = dir_to_save

    def save_image(self):
        # type: () -> None
        """ A function to save the image."""
        if not os.path.exists(self.__dir_to_save):
            os.makedirs(self.__dir_to_save)
        timestamp = (datetime.datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
        filename = (timestamp + ".jpg").replace("/", "-").replace(",", "")
        image = self.__uvc_driver.capture_image()
        cv2.imwrite(os.path.join(self.__dir_to_save, filename), image)

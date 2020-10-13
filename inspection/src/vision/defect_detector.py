#!/usr/bin/python3
import cv2
import numpy as np


class DefectDetector(object):
    """A class to represent a defect detector."""
    def __init__(self):
        # type: () -> None
        """Initialise the class."""
        self.__defect_threshold = 200

    def is_object_defected(self, image, show_window=False):
        # type: (np.ndarray, bool) -> bool
        """A function to check if an object is defected.
        Args:
            image: the image of the object to be examined
            show_window: a bool that indicates whether to show the opencv window or not
        """
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if show_window:
            cv2.imshow('gray', thresh)
        return (thresh > self.__defect_threshold).any()

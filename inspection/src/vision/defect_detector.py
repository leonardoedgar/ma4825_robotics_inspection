#!/usr/bin/python3
from typing import Optional
import cv2
import numpy as np
import math


class DefectDetector(object):
    """A class to represent a defect detector."""
    def __init__(self, camera_params=None):
        # type: (Optional[dict]) -> None
        """Initialise the class."""
        self.__camera_params = camera_params

    def is_object_defected(self, image, show_window=False):
        # type: (np.ndarray, bool) -> bool
        """A function to check if an object is defected.
        Args:
            image: the image of the object to be examined
            show_window: a bool that indicates whether to show the opencv window or not
        """
        # Undistort image
        if self.__camera_params is not None:
            image = cv2.undistort(image, np.array(self.__camera_params["camera_mtx"]),
                                  np.array(self.__camera_params["dist_coef"]),
                                  np.array(self.__camera_params["new_camera_mtx"]))
            image = \
                image[self.__camera_params["roi"]["y"]:
                      self.__camera_params["roi"]["y"] + self.__camera_params["roi"]["height"],
                      self.__camera_params["roi"]["x"]:
                      self.__camera_params["roi"]["x"] + self.__camera_params["roi"]["width"]]

        # Crop image based on region of interest
        height, width = image.shape[:2]
        roi = image[int(height / 3):int(height * 4 / 5),
                    int(width / 4):int(width * 3 / 4), :]
        original_roi = roi.copy()

        # Threshold image
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(cv2.bitwise_not(gray), 200, 255, cv2.THRESH_TOZERO)[1]

        # Find all contours
        contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        min_area = math.pow(10, 5) * 0.2
        max_area = math.pow(10, 5) * 1
        image[:, :, 2] = 0

        # Filter found contours based on area
        for c in contours:
            area = cv2.contourArea(c)
            if min_area < area < max_area:
                cv2.drawContours(roi, [c], -1, (0, 0, 255), -1)
        copied_result = roi.copy()
        mask = np.array(copied_result[:, :, 2])
        mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)[1]
        segmented_object = cv2.bitwise_and(original_roi, original_roi, mask=mask)

        # Threshold segmented object
        gray_segmented = cv2.cvtColor(segmented_object, cv2.COLOR_BGR2GRAY)
        gray_segmented = cv2.threshold(gray_segmented, 70, 255, cv2.THRESH_BINARY)[1]

        # Noise removal
        kernel = np.ones((3, 3), np.uint8)
        gray_segmented = cv2.erode(src=gray_segmented, kernel=kernel, iterations=1)

        # Label results
        is_defected = False
        if (gray_segmented > 254).any():
            is_defected = True
            cv2.putText(original_roi, "DEFECT",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255), 2)
        else:
            cv2.putText(original_roi, "NO DEFECT",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255), 2)

        # Display results
        if show_window:
            cv2.imshow("roi", roi)
            cv2.imshow("segmentation", segmented_object)
            cv2.imshow("defect", gray_segmented)
            cv2.imshow("labelled", original_roi)
        return is_defected

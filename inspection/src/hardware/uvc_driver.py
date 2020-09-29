#!/usr/bin/python3
import cv2
from typing import Optional
from exception.exception import HardwareException


class UVCDriver(object):
    """A class to represent UVC video driver."""
    def __init__(self, video_device_id, frame_res=None, fps=None):
        # type: (int, Optional[tuple], float) -> None
        """
        Initialise the class.
        Args:
            video_device_id: the video device id as indicated by Linux kernel to open the UVC driver from
            frame_res: the frame resolution to capture and save the video with
            fps: the frame rate to capture and save the video with
        """
        self.__capturer = cv2.VideoCapture(video_device_id)  # type: cv2.VideoCapture

        # temporary fix on OpenCV bug https://github.com/opencv/opencv/issues/9477
        self.__capturer.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))

        if frame_res is not None:
            self.__capturer.set(cv2.CAP_PROP_FRAME_WIDTH, frame_res[0])
            self.__capturer.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_res[1])
        if fps is not None:
            self.__capturer.set(cv2.CAP_PROP_FPS, fps)
        self.__captured_image = None

    def start(self, window_name="image"):
        # type: (str) -> None
        """A function to start the video streaming from the video driver.
        Args:
            window_name: the window name to be showed on OpenCV GUI.
        """
        while self.__capturer.isOpened():
            ret, self.__captured_image = self.__capturer.read()
            if ret:
                cv2.imshow(window_name, self.__captured_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

    def capture_image(self):
        """A function to capture an image from the uvc video driver."""
        if self.__captured_image is None:
            raise HardwareException("uvc driver has not been opened yet to capture image.")
        return self.__captured_image

    def release(self):
        # type: () -> None
        """A function to release the resources of the uvc device."""
        self.__capturer.release()
        cv2.destroyAllWindows()

#!/usr/bin/python3
from hardware.uvc_driver import UVCDriver
from exception.exception import HardwareException
import cv2
import os
import threading
import time


def post_process_image():
	while True:
		try:
			image = uvc_driver.capture_image()
			gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			ret, thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
			# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			cv2.imshow('gray', thresh)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		except HardwareException as err:
			print("Err: %s" % err)
			time.sleep(0.5)
		except KeyboardInterrupt:
			break


if __name__ == '__main__':
	uvc_driver = UVCDriver(
		video_device_id=int(os.getenv("VIDEO_DEVICE_ID")),
		frame_res=(1280, 960))
	uvc_thread = threading.Thread(target=uvc_driver.start)
	image_processor_thread = threading.Thread(target=post_process_image)
	uvc_thread.start()
	image_processor_thread.start()
	uvc_thread.join()
	image_processor_thread.join()
	uvc_driver.release()
	time.sleep(1)

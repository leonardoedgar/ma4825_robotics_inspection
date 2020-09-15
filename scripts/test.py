import numpy as np
import cv2
import time
import os


if __name__ == '__main__':
	cap = cv2.VideoCapture(int(os.environ["VIDEO_DEVICE_ID"]))
	start_time = time.time()
	desired_fps = 60
	resolution = (1280, 960)

	# cap.set(cv2.CAP_PROP_FPS, desired_fps)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
	print("Theoretical FPS: ", cap.get(cv2.CAP_PROP_FPS))
	writer = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 20, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
	captured_frames = []
	num_frames = 0
	while True:
		try:
			ret, frame = cap.read()
			writer.write(frame)
			num_frames += 1

		# Capture frame-by-frame
		# ret, frame = cap.read()

		# Display the resulting frame
		# cv2.imshow('frame', frame)
		# captured_frames.append(frame)

		# if cv2.waitKey(1) & 0xFF == ord('q'):
			# break
		except KeyboardInterrupt:
			break

	# When everything done, release the capture
	end_time = time.time()

	# cv2.destroyAllWindows()
	actual_fps = num_frames/(end_time-start_time)
	print("Actual FPS: ", actual_fps)

	# for frame in captured_frames:
		# writer.write(frame)
	cap.release()
	writer.release()

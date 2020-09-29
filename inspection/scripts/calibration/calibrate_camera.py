#!/usr/bin/python3
from calibration.camera_calibrator import CameraCalibrator
import os
import calibration


if __name__ == '__main__':
    calib_data_dir = os.path.join(os.path.dirname(calibration.__file__), "data")
    camera_calibrator = CameraCalibrator(
        original_images_path=os.path.join(calib_data_dir, "original"),
        undistorted_image_path=os.path.join(calib_data_dir, "undistorted"),
        camera_params_path=os.path.join(os.path.dirname(calibration.__file__), "config", "intrinsic"))
    camera_calibrator.calibrate()
    camera_calibrator.save_undistorted_images()
    camera_calibrator.export_camera_params()

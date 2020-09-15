import numpy as np
import cv2
import glob
import os
from inspection.exception import CalibrationException
import datetime
import yaml


class CameraCalibrator(object):
    def __init__(self, original_images_path, undistorted_image_path, camera_params_path):
        self.__undistorted_image_path = undistorted_image_path
        self.__original_image_filenames = glob.glob(os.path.join(original_images_path, "*.jpg"))
        self.__camera_params_path = camera_params_path
        self.__camera_params = {}
        self.__annotated_original_images = []

    def calibrate(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Check board size
        cbrow = 6
        cbcol = 9

        # prepare object points
        objp = np.zeros((cbrow * cbcol, 3), np.float32)
        objp[:, :2] = np.mgrid[0:cbcol, 0:cbrow].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        obj_points = []  # 3d point in real world space
        img_points = []  # 2d points in image plane.

        height, width = cv2.imread(self.__original_image_filenames[0], 0).shape[:2]

        for image_filename in self.__original_image_filenames:
            gray_img = cv2.imread(image_filename, 0)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray_img, (cbcol, cbrow), None)

            # If found, add object points, image points (after refining them)
            if ret:
                obj_points.append(objp)

            corners2 = cv2.cornerSubPix(gray_img, corners, (11, 11), (-1, -1), criteria)
            img_points.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(gray_img, (cbcol, cbrow), corners2, ret)
            self.__annotated_original_images.append(img)

        rms_error, mtx, dist_coe, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points,
                                                                     (width, height),
                                                                     None, None)
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist_coe, (width, height), 1, (width, height))
        new_camera_mtx = np.hstack((new_camera_mtx, np.zeros((3, 1))))

        self.__camera_params["resolution"] = {"width": width, "height": height}
        self.__camera_params["camera_mtx"] = mtx
        self.__camera_params["dist_coef"] = dist_coe
        self.__camera_params["new_camera_mtx"] = new_camera_mtx
        self.__camera_params["rms_error"] = rms_error

    def save_undistorted_images(self):
        if not self.__annotated_original_images:
            raise CalibrationException("Unable to find annotated calibration images. Ensure to "
                                       "calibrate using images before calling this method.")
        if not os.path.exists(self.__undistorted_image_path):
            os.makedirs(self.__undistorted_image_path)
        else:
            files = glob.glob(os.path.join(self.__undistorted_image_path, "*"))
            for file in files:
                os.remove(file)
        for index, image_filename in enumerate(self.__original_image_filenames):
            undistorted_image = cv2.undistort(self.__annotated_original_images[index], self.__camera_params["camera_mtx"],
                                              self.__camera_params["dist_coef"],
                                              self.__camera_params["new_camera_mtx"])
            cv2.imwrite(os.path.join(self.__undistorted_image_path, os.path.basename(image_filename)),
                        undistorted_image)

    def export_camera_params(self):
        if not self.__camera_params:
            raise CalibrationException("Unable to find calibrated camera params. Camera is uncalibrated.")
        timestamp = (datetime.datetime.now()).strftime("%m/%d/%Y/%H:%M:%S")
        output_filename = os.path.join(self.__camera_params_path, (timestamp + ".yaml").replace("/", "-"))
        with open(output_filename, 'w') as file:
            yaml.dump(self.__camera_params, file, default_flow_style=None)
        print("output filename: %s" % output_filename)

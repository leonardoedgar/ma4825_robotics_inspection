#!/usr/bin/python3 
from calibration.camera_calibrator import CameraCalibrator
import os
import numpy as np

HOME = "/home/leonardo"
UNDISTORTED_IMAGES_PATH = os.path.join(HOME, "undistorted_images")
CAMERA_PARAMS_PATH = os.path.join(HOME, "camera_params")
TEST_IMAGE_FILENAME = "test.jpg"


def get_mocked_camera_calibrator(mocker):
    home = "/home/leonardo"
    original_images_path = os.path.join(home, "original_images")
    mocker.patch("glob.glob", return_value=[os.path.join(original_images_path, TEST_IMAGE_FILENAME)])
    undistorted_images_path = os.path.join(home, "undistorted_images")
    camera_params_path = os.path.join(home, "camera_params")
    camera_calibrator = CameraCalibrator(
        original_images_path=original_images_path,
        undistorted_image_path=undistorted_images_path,
        camera_params_path=camera_params_path)
    camera_calibrator.__annotated_original_images = mocker.MagicMock()
    camera_calibrator.__annotated_original_images.return_value = [np.ones((3, 3))]
    mocker.patch("cv2.imread", return_value=np.ones((3, 3, 3)))
    mocker.patch("cv2.findChessboardCorners", return_value=[True, None])
    mocker.patch("cv2.cornerSubPix")
    mocker.patch("cv2.drawChessboardCorners")
    mocker.patch("cv2.calibrateCamera", return_value=[None, None, None, None, None])
    mocker.patch("cv2.getOptimalNewCameraMatrix", return_value=[None, None])
    mocker.patch("numpy.hstack", return_value=None)
    camera_calibrator.calibrate()
    return camera_calibrator


def test_save_undistorted_images(mocker):
    camera_calibrator = get_mocked_camera_calibrator(mocker)
    mocker.patch("os.path.exists", return_value=False)
    mocked_makedirs = mocker.patch("os.makedirs")
    mocked_imwrite = mocker.patch("cv2.imwrite")
    mocker.patch("cv2.undistort", return_value=[None, None, None, None])
    camera_calibrator.save_undistorted_images()
    assert mocked_makedirs.call_args[0][0] == UNDISTORTED_IMAGES_PATH
    assert mocked_imwrite.call_args[0][0] == os.path.join(UNDISTORTED_IMAGES_PATH, TEST_IMAGE_FILENAME)


def test_export_camera_params(mocker):
    camera_calibrator = get_mocked_camera_calibrator(mocker)
    mocker.patch("yaml.dump")
    mocked_open = mocker.mock_open()
    mocker.patch('builtins.open', mocked_open)
    camera_calibrator.export_camera_params()
    assert CAMERA_PARAMS_PATH in mocked_open.mock_calls[0][1][0]

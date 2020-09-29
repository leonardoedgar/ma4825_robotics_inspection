#!/usr/bin/python3 
from calibration.camera_calibrator import CameraCalibrator
import os
import numpy as np

HOME = "/home/leonardo"
UNDISTORTED_IMAGES_PATH = os.path.join(HOME, "undistorted_images")
CAMERA_PARAMS_PATH = os.path.join(HOME, "camera_params")
TEST_IMAGE_FILENAME = "test.jpg"


def get_mocked_camera_calibrator(mocker):
    """A function to get a mocked camera calibrator."""
    home = "/home/leonardo"
    image_dim = (1280, 960)
    dist_coef = np.array([-0.2713, 0.529, -7.618, 0.0020, -1.15335])
    camera_mtx = np.array([[1361.1001, 0.0, 640.3159],
                           [0.0, 1377.714, 503.3],
                           [0.0, 0.0, 1.0]])
    new_camera_mtx = np.array([[1378.2675, 0.0, 642.0375, 0.0],
                               [0.0, 1385.3125, 502.5054, 0.0],
                               [0.0, 0.0, 1.0, 0.0]])
    rms_error = 0.411
    camera_params = {"resolution": {"width": image_dim[0], "height": image_dim[1]},
                     "camera_mtx": camera_mtx, "new_camera_mtx": new_camera_mtx,
                     "dist_coef": dist_coef, "rms_error": rms_error}
    original_images_path = os.path.join(home, "original_images")
    mocker.patch("glob.glob", return_value=[os.path.join(original_images_path, TEST_IMAGE_FILENAME)])
    undistorted_images_path = os.path.join(home, "undistorted_images")
    camera_params_path = os.path.join(home, "camera_params")
    camera_calibrator = CameraCalibrator(
        original_images_path=original_images_path,
        undistorted_image_path=undistorted_images_path,
        camera_params_path=camera_params_path)
    mocker.patch("cv2.imread", return_value=np.ones((image_dim[1], image_dim[0], 3)))
    mocker.patch("cv2.cvtColor", return_value=np.ones((3, 3)))
    mocker.patch("cv2.findChessboardCorners", return_value=[True, None])
    mocker.patch("cv2.cornerSubPix")
    mocker.patch("cv2.drawChessboardCorners")
    mocker.patch("cv2.calibrateCamera", return_value=[rms_error, camera_mtx, dist_coef, None, None])
    mocker.patch("cv2.getOptimalNewCameraMatrix", return_value=[new_camera_mtx, None])
    camera_calibrator.calibrate()
    return camera_calibrator, camera_params


def test_save_undistorted_images(mocker):
    """A function to test that undistorted images are saved properly."""
    camera_calibrator, camera_params = get_mocked_camera_calibrator(mocker)
    mocker.patch("os.path.exists", return_value=False)
    mocked_makedirs = mocker.patch("os.makedirs")
    mocked_imwrite = mocker.patch("cv2.imwrite")
    mocked_undistort = mocker.patch("cv2.undistort", return_value=[None, None, None, None])
    camera_calibrator.save_undistorted_images()
    assert (mocked_undistort.call_args[0][1] == camera_params["camera_mtx"]).all()
    assert (mocked_undistort.call_args[0][2] == camera_params["dist_coef"]).all()
    assert (mocked_undistort.call_args[0][3] == camera_params["new_camera_mtx"]).all()
    assert mocked_makedirs.call_args[0][0] == UNDISTORTED_IMAGES_PATH
    assert mocked_imwrite.call_args[0][0] == os.path.join(UNDISTORTED_IMAGES_PATH, TEST_IMAGE_FILENAME)


def test_export_camera_params(mocker):
    """A function to test that camera params can be exported to a file."""
    camera_calibrator, camera_params = get_mocked_camera_calibrator(mocker)
    camera_params["camera_mtx"] = camera_params["camera_mtx"].tolist()
    camera_params["dist_coef"] = camera_params["dist_coef"].tolist()
    camera_params["new_camera_mtx"] = camera_params["new_camera_mtx"].tolist()
    mocker.patch("os.path.exists", return_value=False)
    mocked_makedirs = mocker.patch("os.makedirs")
    mocked_dump = mocker.patch("yaml.dump")
    mocked_open = mocker.mock_open()
    mocker.patch('builtins.open', mocked_open)
    camera_calibrator.export_camera_params()
    assert mocked_dump.call_args[0][0] == camera_params
    assert mocked_makedirs.call_args[0][0] == CAMERA_PARAMS_PATH
    assert CAMERA_PARAMS_PATH in mocked_open.mock_calls[0][1][0]

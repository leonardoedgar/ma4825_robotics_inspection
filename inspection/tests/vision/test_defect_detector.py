#!/usr/bin/python3
from vision.defect_detector import DefectDetector
import numpy as np
import pytest
import math


DIST_COEF = np.array([-0.2413, 0.529, -7.618, 0.0020, -1.15335])
CAMERA_MTX = np.array([[1361.1001, 0.0, 640.3159],
                       [0.0, 1377.714, 503.3],
                       [0.0, 0.0, 1.0]])
NEW_CAMERA_MTX = np.array([[1378.2675, 0.0, 642.0375, 0.0],
                           [0.0, 1385.3125, 502.5054, 0.0],
                           [0.0, 0.0, 1.0, 0.0]])
ROI = {"height": 3, "width": 3, "x": 0, "y": 0}

@pytest.mark.parametrize("camera_params", [None,
                                           {"dist_coef": DIST_COEF,
                                            "new_camera_mtx": NEW_CAMERA_MTX,
                                            "camera_mtx": CAMERA_MTX,
                                            "roi": ROI}])
def test_is_object_defected(mocker, camera_params):
    """A function to test that defected object can be recognised."""
    detector = DefectDetector(camera_params=camera_params)
    test_segmented_image = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 255]])
    test_original_image = np.ones((3, 3, 3))
    test_contour = np.array([[1, 2], [3, 4]])
    mocked_undistort = mocker.patch("cv2.undistort", return_value=test_original_image)
    mocked_cvtColor = mocker.patch("cv2.cvtColor", return_value=test_original_image[:, :, 1])
    mocked_threshold = mocker.patch("cv2.threshold",
                                    return_value=[True, test_original_image[:, :, 1]])
    mocker.patch("cv2.findContours", return_value=[np.array([]), test_contour])
    mocker.patch("cv2.contourArea", return_value=math.pow(10, 5)*0.7)
    mocked_drawContours = mocker.patch("cv2.drawContours")
    mocker.patch("cv2.bitwise_and", return_value=test_original_image)
    mocker.patch("cv2.erode", return_value=test_segmented_image)
    mocker.patch("cv2.putText")
    mocker.patch("cv2.imshow")
    assert detector.is_object_defected(image=test_original_image, show_window=True)
    if camera_params is not None:
        assert (mocked_undistort.call_args[0][0] == test_original_image).all()
        assert (mocked_undistort.call_args[0][1] == camera_params["camera_mtx"]).all()
        assert (mocked_undistort.call_args[0][2] == camera_params["dist_coef"]).all()
        assert (mocked_undistort.call_args[0][3] == camera_params["new_camera_mtx"]).all()
    assert (mocked_cvtColor.mock_calls[0][1][0][0] == test_original_image).all()
    assert (mocked_threshold.call_args[0][0] == test_original_image[:, :, 1]).all()
    mocked_drawContours.assert_called()

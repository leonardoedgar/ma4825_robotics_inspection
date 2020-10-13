#!/usr/bin/python3
from vision.defect_detector import DefectDetector
import numpy as np


def test_is_object_defected(mocker):
    """A function to test that defected object can be recognised."""
    detector = DefectDetector()
    test_segmented_image = np.array([[90, 2, 156], [50, 0, 37], [54, 101, 233]])
    test_original_image = np.ones((3, 3, 3))
    mocked_cvtColor = mocker.patch("cv2.cvtColor", return_value=test_original_image[:, :, 1])
    mocked_threshold = mocker.patch("cv2.threshold", return_value=[True, test_segmented_image])
    mocked_imshow = mocker.patch("cv2.imshow")
    assert detector.is_object_defected(image=test_original_image, show_window=True)
    assert (mocked_cvtColor.call_args[0][0] == test_original_image).all()
    assert (mocked_threshold.call_args[0][0] == test_original_image[:, :, 1]).all()
    assert (mocked_imshow.call_args[0][1] == test_segmented_image).all()

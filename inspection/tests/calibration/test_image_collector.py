#!/usr/bin/python3
from calibration.image_collector import ImageCollector
import numpy as np


def get_mocked_image_collector(mocker, dir_to_save=None):
    """A function to get a mocked image collector."""
    mocked_uvc_driver = mocker.MagicMock()
    return ImageCollector(uvc_driver=mocked_uvc_driver, dir_to_save=dir_to_save), mocked_uvc_driver


def test_save_image(mocker):
    """A function to test that image collector can save image."""
    mocker.patch('os.path.exists', return_value=False)
    mocked_makedirs = mocker.patch('os.makedirs')
    mocked_imwrite = mocker.patch("cv2.imwrite")
    dir_to_save = "/home/leonardo/inspection/data/original"
    image_collector, mocked_uvc_driver = get_mocked_image_collector(mocker, dir_to_save)
    image_to_save = np.ones((5, 5))
    mocked_uvc_driver.capture_image.return_value = image_to_save
    image_collector.save_image()
    assert mocked_makedirs.call_args[0][0] == dir_to_save
    assert dir_to_save in mocked_imwrite.call_args[0][0]
    assert (mocked_imwrite.call_args[0][1] == image_to_save).all()

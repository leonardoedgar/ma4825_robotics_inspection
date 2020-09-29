#!/usr/bin/python3 
from hardware.uvc_driver import UVCDriver
from exception.exception import HardwareException
import pytest
import numpy as np
import cv2


def get_mocked_uvc_driver(mocker, video_device_id, frame_res=None, fps=None):
    """A function to get a mocked uvc driver."""
    mocked_video_capture = mocker.patch('cv2.VideoCapture')
    return UVCDriver(video_device_id=video_device_id, frame_res=frame_res, fps=fps), mocked_video_capture


@pytest.mark.parametrize("video_device_id, frame_res, fps", [(0, None, None), (2, (1280, 960), 10)])
def test_initialisation(mocker, video_device_id, frame_res, fps):
    """A function to test that uvc driver can be initialised."""
    uvc_driver, mocked_video_capture = \
        get_mocked_uvc_driver(mocker, video_device_id=video_device_id, frame_res=frame_res, fps=fps)
    assert mocked_video_capture.call_args[0][0] == video_device_id
    if frame_res is not None:
        assert mocked_video_capture().set.mock_calls[1][1] == (cv2.CAP_PROP_FRAME_WIDTH, frame_res[0])
        assert mocked_video_capture().set.mock_calls[2][1] == (cv2.CAP_PROP_FRAME_HEIGHT, frame_res[1])
    if fps is not None:
        assert mocked_video_capture().set.mock_calls[3][1] == (cv2.CAP_PROP_FPS, fps)


def test_start(mocker):
    """A function to test that uvc driver can start the video streaming."""
    mocked_cv2_imshow = mocker.patch('cv2.imshow')
    uvc_driver, mocked_video_capturer = get_mocked_uvc_driver(mocker, video_device_id=0)
    image_frame = np.ones((40, 40))
    mocked_video_capturer().isOpened.side_effect = [True, False]
    mocked_video_capturer().read.return_value = True, image_frame
    uvc_driver.start()
    mocked_video_capturer().read.assert_called_once()
    assert (mocked_cv2_imshow.call_args[0][1] == image_frame).all()


@pytest.mark.parametrize("captured_image", [None, np.ones((5, 5))])
def test_capture_image(mocker, captured_image):
    """A function to test that uvc driver is able to capture an image from a video stream."""
    mocker.patch('cv2.imshow')
    uvc_driver, mocked_video_capturer = get_mocked_uvc_driver(mocker, video_device_id=0)
    mocked_video_capturer().isOpened.side_effect = [True, False]
    mocked_video_capturer().read.return_value = True, captured_image
    uvc_driver.start()
    if captured_image is None:
        with pytest.raises(HardwareException):
            uvc_driver.capture_image()
    else:
        assert (captured_image == uvc_driver.capture_image()).all()


def test_release(mocker):
    """A function to test that resources of the uvc device can be released."""
    mocked_cv2_destroy_all_windows = mocker.patch('cv2.destroyAllWindows')
    uvc_driver, mocked_video_capturer = get_mocked_uvc_driver(mocker, video_device_id=0)
    uvc_driver.release()
    mocked_video_capturer().release.assert_called_once()
    mocked_cv2_destroy_all_windows.assert_called_once()

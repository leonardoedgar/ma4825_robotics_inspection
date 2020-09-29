#!/usr/bin/python3
from typing import Optional


class CalibrationException(Exception):
    """A class to represent the exception in the calibration package."""
    def __init__(self, error_msg="Calibration Error"):
        # type: (Optional[str]) -> None
        """Initialise the class.
        Args:
            error_msg: error message to show.
        """
        super(CalibrationException, self).__init__(error_msg)


class HardwareException(Exception):
    """A class to represent the exception in the hardware package."""
    def __init__(self, error_msg="Hardware Error"):
        # type: (Optional[str]) -> None
        """Initialise the class.
        Args:
            error_msg: error message to show.
        """
        super(HardwareException, self).__init__(error_msg)

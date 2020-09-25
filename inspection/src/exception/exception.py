class CalibrationException(Exception):
    def __init__(self, error_msg="Calibration Error"):
        super(CalibrationException, self).__init__(error_msg)

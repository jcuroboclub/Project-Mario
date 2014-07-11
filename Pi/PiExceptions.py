class BaseException(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return repr(self._msg)

class SerialPortException(BaseException):
    def __init__(self, msg):
        super().__init__(msg)

class ThreadException(BaseException):
    def __init__(self, msg):
        super().__init__(msg)

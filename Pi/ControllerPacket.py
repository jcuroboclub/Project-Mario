class ControllerPacket():

    DELIMITER = b','

    def __init__(self, controllerNumber, byteArray):
        
        self._controllerNumber = controllerNumber

        # Not sure what the controller packet data looks like at this stage
        self._data = byteArray.strip().split(ControllerPacket.DELIMITER)

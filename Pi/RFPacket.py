class RFPacket:

    DELIMITER = b','
    
    def __init__(self, byteArray):

        split = byteArray.split(RFPacket.DELIMITER)

        self._command = split[0];

        self._data = split[1:]


    def __init__(self, command, dataArray):
        # Runs on the assumption that command and the data variables
        # are passed in as bytes and an array of bytes respectively
        self._command = command

        self.setData(dataArray)

    def getCommand(self):
        return self._command

    def getData(self):
        return self._data

    def setCommand(self, command):
        self._command = command

    def setData(self, dataArray):
        self._data = dataArray
            
    def getByteOutput(self):
        output = self._command

        for datum in self._data:
            output += b',' + datum

        return output


if __name__ == "__main__":
    command = b'command'
    data1 = b'data1'
    data2 = b'data2'
    data3 = b'data3'

    packet1 = RFPacket(command, data1)
    packet2 = RFPacket(command, data1, data2, data3)

    packet1.getByteOutput()
    packet2.getByteOutput()
    packet3.getByteOutput()
        

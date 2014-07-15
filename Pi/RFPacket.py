class RFPacket:

    DELIMITER = b','
    
    def __init__(self, byteArray):

        split = byteArray.split(RFPacket.DELIMITER)

        self._command = split[0];

        self._data = split[1:]


    def __init__(self, command, *arg):
        # Runs on the assumption that command and the data variables
        # are passed in as bytes
        self._command = command

        intrimData = list()
        
        for datum in arg:
            intrimData.append(datum)

        self.setData(intrimData)

    def getCommand(self):
        return self._command

    def getData(self):
        return self._data

    def setCommand(self, command):
        self._command = command

    def setData(self, *arg):
        self._data = []

        # Loop through the data and append it to the data array
        for datum in arg:
            # Check to see if input was a data array
            if type(datum) is list:
                for listDatum in datum:
                    self._data.append(listDatum)
            else:
                self._data.append(datum)
            

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
    dataArray = [b'data1', b'data2', b'data3']

    packet1 = RFPacket(command, data1)
    packet2 = RFPacket(command, data1, data2, data3)
    packet3 = RFPacket(command, dataArray)

    packet1.getByteOutput()
    packet2.getByteOutput()
    packet3.getByteOutput()
        

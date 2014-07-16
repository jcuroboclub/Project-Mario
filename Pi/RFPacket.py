class RFPacket:

    DELIMITER = b','
    ENCODING = "UTF-8"
    
    def __init__(self, *args, **kwargs):
        """Create an RFPacket.

        Arguments:
        1 Argument   -- A bytes object in the format 'target,command,data1,data2...'
        3 Arguments  -- First:   Target   (as a bytes object)
                        Second:  Command  (as a bytes object)
                        Third:   Data     (as an array of bytes objects)

        Shit will break if you don't use that convention at this stage
        """

        if len(args) == 1:
            split = args[0].split(RFPacket.DELIMITER)

            self._targetNumber = split[0]
            self._command = split[1]

            if len(split) > 2:
                self.setData(split[2:])
            else:
                self.setData([])
                
        else:
            self._targetNumber = args[0]
            
            self._command = args[1]

            self.setData(args[2])

    def __bytes__(self):
        output = self._targetNumber + RFPacket.DELIMITER + self._command

        for datum in self._data:
            output += RFPacket.DELIMITER + datum
            
        return output

    def __str__(self):
        # Many used for visualisation and not an actual string representation of the packet

        target = self._targetNumber.decode(ENCODING)
        command = self._command.decode(ENCODING)
        
        data = []
        for datum in self._data:
            data.append(datum.decode(ENCODING))
        
        return str.format("Target: {0}\nCommand: {1}\nContent: {2}", target, command, data)

    def getTarget(self):
        return self._targetNumber
    
    def getCommand(self):
        return self._command

    def getData(self):
        return self._data

    def setTarget(self, target):
        self._targetNumber = target
        
    def setCommand(self, command):
        self._command = command

    def setData(self, dataArray):
        self._data = dataArray

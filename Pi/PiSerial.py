import serial
from PiExceptions import *
from queue import Queue
from threading import Thread

class SerialPort:

    __QUEUE_SIZE = 256
    
    def __init__(self, portNumber, baudRate):

        # Decrement the port number as the serial module starts
        # count at 0
        self._portNumber = portNumber - 1
        self._baudRate = baudRate
        
        self._receiveQueue = Queue(SerialPort.__QUEUE_SIZE)

        # Thread, Comm, and thread flag initialisation
        self.reset()

    def openPort(self):
        if self._serialPort is not None and self._serialPort.isOpen():
            raise SerialPortException("Serial Port is already openned.")

        self._serialPort = serial.Serial(self._portNumber, self._baudRate)

    def beginReceiving(self):
        if self._serialPort is None:
            raise SerialPortException("Serial Port hasn't been initialised.")

        if self._communicationThread is not None:
            raise ThreadException("A communication thread is already running.")
            
        self._communicationThread = Thread(target=self.read)
        self._communicationThread.daemon = True
        self._communicationThread.start()
        
    def read(self):
        while not self._killThread:
            # If the queue becomes full (hasn't been read from in ages)
            # discard the oldest item
            if self._receiveQueue.full():
                self._receiveQueue.get()
                
            self._receiveQueue.put(self._serialPort.readline());
            
    def readBuffer(self):
        # Should think of what is the best output format for this
        # Just going to use an array at this stage

        output = list()
        while not self._receiveQueue.empty():
            output.append(self._receiveQueue.get())

        return output

    def reset(self):
        # Initialise the serial port and comm thread to null
        self._serialPort = None
        self._communicationThread = None

        # Initiaise the thread termination flag
        self._killThread = False
        
    def closePort(self):
        if self._serialPort is None or not self._serialPort.isOpen():
            raise SerialPortException("Serial Port is either already closed or not initialised.")
        
        while self._communicationThread and self._communicationThread.isAlive():
            self._killThread = True
      
        self._serialPort.close()

        self.reset()


if __name__ == "__main__":
    test = SerialPort(8,9600)
    test.openPort()
    test.beginReceiving()
    input("Wait a second to collect some data\n")
    data = test.readBuffer()
    for datum in data:
        print(datum)
    test.closePort()
        

    

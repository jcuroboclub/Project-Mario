from subprocess import check_output, call
from PiSerial import SerialPort

class CommunicationModule:
    # Write pi user pwd into this file, to allow sudo calls without pwd prompts
    # It's dirty but it works
    PWD_LOCATION = "~/test/pwd"
    USB_DIR = "/dev/ttyACM"
    ENCODING = "UTF-8"
    BAUD_RATE = 9600

    def getConnectedUSBLocations(self):

        connectedUSB = check_output(str.format('ls {0}*', CommunicationModule.USB_DIR),
                                    shell=True).strip()

        USBList = connectedUSB.split(b'\n')

        return USBList

    def setUSBPermissions(self, USBLocation):
        call(str.format("sudo chmod 666 {0} < {1}", USBLocation.decode(CommunicationModule.ENCODING),
                        CommunicationModule.PWD_LOCATION), shell=True)

    def initialiseUSB(self):

        USBList = self.getConnectedUSBLocations()

        self._portDict = dict()
        
        for USB in USBList:
            self.setUSBPermissions(USB)

            portNumber = int(USB.lstrip(bytes(CommunicationModule.USB_DIR,
                                              CommunicationModule.ENCODING)))
            self._portDict[portNumber] = SerialPort(portNumber, CommunicationModule.BAUD_RATE)

    def main(self):

        self.initialiseUSB()
        
        while True:
            for key in self._portDict.keys():
                print("Port: " + str(key))
                
                for datum in self._portDict[key].readBuffer():
                    print(datum)

            input("Press key to grab data...\n")

if __name__ == "__main__":
    module = CommunicationModule()
    module.main()

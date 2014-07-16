from subprocess import check_output, call
from PiSerial import SerialPort

class CommunicationModule:
    # Write pi user pwd into this file, to allow sudo calls without pwd prompts
    # It's dirty but it works
    pwdLocation = "~/test/pwd"
    USBDir = "/dev/ttyACM"
    encoding = "UTF-8"
    baudRate = 9600

    def getConnectedUSBLocations(self):

        connectedUSB = check_output(str.format('ls {0}*', USBDir), shell=True).strip()

        USBList = connectedUSB.split(b'\n')

        return USBList

    def setUSBPermissions(self, USBLocation):
        call(str.format("sudo chmod 666 {0} < {1}", USBLocation.decode(encoding),
                        pwdLocation), shell=True)

    def initialiseUSB(self):

        USBList = self.getConnectedUSBLocations()

        self._portDict = dict()
        
        for USB in USBList:
            self.setUSBPermissions(USB)

            portNumber = int(USB.lstrip(bytes(USBDir, encoding)))
            self._portDict[portNumber] = SerialPort(portNumber, baudRate)

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

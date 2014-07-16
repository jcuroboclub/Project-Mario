from subprocess import check_output, call
from PiSerial import SerialPort

class CommunicationModule:
    # Write pi user pwd into this file, to allow sudo calls without pwd prompts
    # It's dirty but it works
    pwdLocation = "~/test/pwd"
    USBDir = "/dev/ttyACM"
    encoding = "UTF-8"
    baudRate = 9600

    def getConnectedUSBLocations():

        connectedUSB = check_output(str.format('ls {0}*', USBDir), shell=True).strip()

        USBList = connectedUSB.split(b'\n')

        return USBList

    def setUSBPermissions(USBLocation):
        call(str.format("sudo chmod 666 {0} < {1}", USBLocation.decode(encoding),
                        pwdLocation), shell=True)

    def initialiseUSB():

        USBList = getConnectedUSBLocations()

        self._portDict = dict()
        
        for USB in USBList:
            setUSBPermissions(USB)

            portNumber = int(USB.lstrip(bytes(USBDir, encoding)))
            self._portDict[portNumber] = SerialPort(portNumber, baudRate)

    def main():

        initialiseUSB()


if __name__ == "__main__":
    module = CommunicationModule()
    module.main()

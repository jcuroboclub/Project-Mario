from subprocess import check_output, call
import PiSerial

# Write pi user pwd into this file, to allow sudo calls without pwd prompts
pwdLocation = "~/test/pwd"

def getConnectedUSBLocations():

    connectedUSB = check_output('ls /dev/ttyACM*', shell=True).strip()

    USBList = connectedUSB.split(b'\n')

    return USBList

def setUSBReadable(USBLocation):
    call(str.format("sudo chmod 666 {0} < {1}", USBLocation.decode('utf-8'), pwdLocation), shell=True)

def initialiseUSB():

    USBList = getConnectedUSBLocations()

    for USB in USBList:
        setUSBReadable(USB)

def main():

    initialiseUSB()


if __name__ == "__main__":
    main()

import unittest
from RFPacket import RFPacket

class RFPacketTest(unittest.TestCase):

    BYTE_ARRAY_ONE = b'0,Control,X,O,O,X'

    TARGET_ONE = b'0'
    COMMAND_ONE = b'Control'
    DATA_ONE = [b'X', b'O', b'O', b'X']

    TARGET_TWO = b'1'
    COMMAND_TWO = b'Stop'
    DATA_TWO = [b'O', b'O', b'X', b'O']

    def setUp(self):
        self._packetOne = RFPacket(RFPacketTest.BYTE_ARRAY_ONE)
        self._packetThree = RFPacket(RFPacketTest.TARGET_ONE,
                                     RFPacketTest.COMMAND_ONE,
                                     RFPacketTest.DATA_ONE)

    def testInitialisation(self):
        self.assertEqual(bytes(self._packetOne), RFPacketTest.BYTE_ARRAY_ONE)
        self.assertEqual(bytes(self._packetThree), RFPacketTest.BYTE_ARRAY_ONE)

    def testTargetGetterSetter(self):
        self.assertEqual(self._packetOne.getTarget(), RFPacketTest.TARGET_ONE,
                         "Packet getTarget method failed.")

        self._packetOne.setTarget(RFPacketTest.TARGET_TWO)

        self.assertEqual(self._packetOne.getTarget(), RFPacketTest.TARGET_TWO,
                         "Packet setTarget method failed.")

    
    def testCommandGetterSetter(self):
        self.assertEqual(self._packetOne.getCommand(), RFPacketTest.COMMAND_ONE,
                         "Packet getCommand method failed.")

        self._packetOne.setCommand(RFPacketTest.COMMAND_TWO)

        self.assertEqual(self._packetOne.getCommand(), RFPacketTest.COMMAND_TWO,
                         "Packet setCommand method failed.")
    
    def testDataGetterSetter(self):
        self.assertEqual(self._packetOne.getData(), RFPacketTest.DATA_ONE,
                         "Packet getData method failed.")

        self._packetOne.setData(RFPacketTest.DATA_TWO)

        self.assertEqual(self._packetOne.getData(), RFPacketTest.DATA_TWO,
                         "Packet setData method failed.")



if __name__ == "__main__":
    unittest.main()

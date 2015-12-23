"""This module implements a serial bus class which talks to bioloid
devices through a serial port.

"""

import serial
import select

class SerialPort(object):
    """Implements a PySerial port for use with the Bioloid Bus.

    """

    def __init__(self, port, baud=1000000):
        self.serial_port = serial.Serial(port=port,
                                         baudrate=baud,
                                         timeout=0.1,
                                         bytesize=serial.EIGHTBITS,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         xonxoff=False,
                                         rtscts=False,
                                         dsrdtr=False)

    def is_byte_available(self):
        readable, _, _ = select.select([self.serial_port.fileno()], [], [], 0)
        return bool(readable)

    def read_byte(self):
        """Reads a byte from the bus. This function will return None if
        no character was read within the designated timeout.

        The max Return Delay time is 254 x 2 usec = 508 usec (the
        default is 500 usec). This represents the minimum time between
        receiving a packet and sending a response.

        """
        data = self.serial_port.read()
        if data:
            return data[0]
        return None

    def write_packet(self, packet_data):
        """Function implemented by a derived class which actually writes
        the data to a device.

        """
        self.serial_port.write(packet_data)

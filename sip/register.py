import serial

from iota.storage import Storage, Word, NounType
from sip.reliable import ReliableConnection

class SerialEvalRegister:
    @staticmethod
    def allocate_zero(port):
        return SerialEvalRegister.allocate(port, Word(0, o=NounType.INTEGER))

    @staticmethod
    def allocate(port, i):
        return SerialEvalRegister(port, i)

    def __init__(self, port, i):
        self.port = port
        self.conn = ReliableConnection(serial.Serial(port, baudrate=115200))
        self.i = i
        self.r = None

    def store_i(self, i):
        self.i = i

    def fetch_i(self):
        return self.i

    def fetch_r(self):
        return self.r

    def load_i(self, d):
        (x, rest) = Storage.from_bytes(d)
        if len(rest) == 0:
            self.store_i(x)
        else:
            raise Exception("bad decode, %d bytes leftover" % len(rest))

    def retrieve_r(self):
        x = self.fetch_r()
        data = x.to_bytes()
        return data

    def eval(self):
        self.i.to_conn(self.conn)
        self.r = Storage.from_conn(self.conn)

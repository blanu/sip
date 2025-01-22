import serial

from iota.api import Object
from iota.storage import Storage, Word, NounType, StorageType

class SerialEvalRegister:
    @staticmethod
    def allocate_zero(port):
        return SerialEvalRegister.allocate(port, Word(0, o=NounType.INTEGER))

    @staticmethod
    def allocate(port, i):
        return SerialEvalRegister(port, i)

    def __init__(self, port, i):
        self.port = port
        self.conn = serial.Serial(port, baudrate=9600)
        self.i = i
        self.r = None

    def conn_read(self):
        storageType = self.readOne()
        objectType = self.readOne()
        if storageType[0] == StorageType.WORD:
            lengthBytes = self.readOne()
            lengthByte = lengthBytes[0]
            length = int(lengthByte)
            if length & 0x80:
                length = length & 0x7F
            rest = self.read(length)
        return storageType + objectType + lengthBytes + rest

    def readOne(self):
        result = b''
        while len(result) == 0:
            result = self.conn.read(1)
        return result

    def read(self, size):
        result = b''
        while len(result) < size:
            result += self.readOne()

        return result

    def write(self, bytes):
        self.conn.write(bytes)
        self.conn.flush()

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
        i_data = self.i.to_bytes()
        self.conn.write(i_data)
        r_data = self.conn_read()
        result = Object.from_bytes(r_data)
        self.r = result[0]

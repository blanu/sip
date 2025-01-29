class ReliableConnection:
    def __init__(self, unreliable):
        self.unreliable = unreliable

    def readOne(self):
        result = b''
        while len(result) == 0:
            result = self.unreliable.read(1)
        return result

    def read(self, size):
        result = b''
        while len(result) < size:
            result += self.unreliable.read(size - len(result))

        return result

    def readType(self):
        result = self.read(2)
        while result[0] == 0x80:
            print("DEBUG: " + result[1:].hex())
            result = self.read(2)
        return result[0], result[1]

    def write(self, bytes):
        self.unreliable.write(bytes)
        self.unreliable.flush()

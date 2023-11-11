from encryption import Encryption
from image import ImageTools


def bytes_to_string(data):
    b = bytearray(data)
    res = ''.join("{:08b}".format(x) for x in b)
    return res


class Utility:
    def __init__(self, args):
        self.args = args

    def decode(self):
        image = ImageTools(self.args)
        encryptor = Encryption(self.args)
        binary_header = image.extract_binary_header()
        name, size, bits, offset = encryptor.decrypt_header(binary_header)
        binary_data = image.extract_binary_data(size, bits, offset)
        encryptor.decrypt_data(binary_data, name)

    def encode(self):
        encryptor = Encryption(self.args)
        data, header = encryptor.encrypt(self.args.encode)
        data = bytes_to_string(data)
        header = bytes_to_string(header)
        image = ImageTools(self.args)
        image.hide_binary_data(data, header)

from cryptography.fernet import Fernet
import os
import sys


class Encryption:
    def __init__(self, args):
        self.args = args
        if self.args.key:
            if len(self.args.key) != 44 or self.args.key[-1] != '=':
                print(f"key must be of length 44 and end with an '=' key length was {len(self.args.key)}")
                sys.exit()
            self.key = self.args.key.encode()
        else:
            self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def encrypt(self, file):
        print(f"encrypting using {self.key.decode()} as key")
        print("saving key to key file...")
        with open('key.key', 'wb') as file_key:
            file_key.write(self.key)
        with open(file, 'rb') as file_byte:
            data = file_byte.read()
        encrypted_data = self.fernet.encrypt(data)
        data_size = len(encrypted_data)
        file = '"' + os.path.basename(file) + '"'
        header_data = f"{file} {data_size} {self.args.bits} {self.args.offset}"
        encrypted_header_data = self.fernet.encrypt(header_data.encode())
        return encrypted_data, encrypted_header_data + '/?/?/?/'.encode()

    def decrypt_header(self, data):
        try:
            decrypted = self.fernet.decrypt(data)
        except Exception as e:
            print("Incorrect Key")
            sys.exit()
        decoded_data = decrypted.decode()
        name = decoded_data[1:decoded_data.rfind('"')]
        decoded_data = decoded_data[decoded_data.rfind('"')+1:].split()
        size = int(decoded_data[0]) * 8
        bits = int(decoded_data[1])
        offset = int(decoded_data[2])
        return name, size, bits, offset

    def decrypt_data(self, data, name):
        decrypted = self.fernet.decrypt(data)
        if self.args.save:
            file_type = ''
            if name.rfind('.') > 0:
                file_type = name[name.rfind('.'):]
            name = self.args.save + file_type
        with open(name, 'wb') as dec_file:
            dec_file.write(decrypted)

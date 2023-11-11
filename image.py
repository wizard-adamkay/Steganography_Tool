from PIL import Image
import sys


class ImageTools:
    def __init__(self, args):
        self.args = args
        if self.args.decode:
            self.image = Image.open(self.args.decode)
        else:
            self.image = Image.open(self.args.target)
            if self.image.mode != 'RGBA':
                print("no alpha channel found on image, adding one")
                self.image.putalpha(255)
        self.width, self.height = self.image.size

    def alter_end(self, val, data, index, header):
        if header:
            self.args.bits = 1
        if len(data) <= index:
            return val, index
        binary_old = "{:08b}".format(val)
        binary_new = binary_old[:8 - self.args.bits] + data[index:index + self.args.bits]
        while len(binary_new) != 8:
            binary_new += "0"
        index += self.args.bits
        return int(binary_new, 2), index

    def hide_binary_data(self, data, header):
        index = 0
        for y in range(self.height - 5):
            for x in range(self.width):
                if x % self.args.offset != 0:
                    continue
                r, g, b, a = self.image.getpixel((x, y))
                r, index = self.alter_end(r, data, index, False)
                g, index = self.alter_end(g, data, index, False)
                b, index = self.alter_end(b, data, index, False)
                a, index = self.alter_end(a, data, index, False)
                self.image.putpixel((x, y), (r, g, b, a))
        if index < len(data):
            print("!!!message data too large for file, aborting!!!")
            print(f"!!!only {int(index/len(data)*100)}% of the data could be stored!!!")
            sys.exit()
        print(f"data stored! used {int(len(data) / ((self.width * (self.height - 5) / self.args.offset) * self.args.bits * 4) * 100)}% of space available")
        index = 0
        for y in range(self.height - 5, self.height):
            for x in range(self.width):
                r, g, b, a = self.image.getpixel((x, y))
                r, index = self.alter_end(r, header, index, True)
                g, index = self.alter_end(g, header, index, True)
                b, index = self.alter_end(b, header, index, True)
                a, index = self.alter_end(a, header, index, True)
                self.image.putpixel((x, y), (r, g, b, a))
        if index < len(header):
            print("!!!message header too large for file, aborting!!!")
            sys.exit()
        index = self.args.save.rfind('.')
        if index != -1:
            self.args.save = self.args.save[:index]
        self.image.save(self.args.save + ".png")

    def extract_binary_header(self):
        str_header = ''
        for y in range(self.height - 5, self.height):
            for x in range(self.width):
                r, g, b, a = self.image.getpixel((x, y))
                str_header += "{:08b}".format(r)[7:]
                str_header += "{:08b}".format(g)[7:]
                str_header += "{:08b}".format(b)[7:]
                str_header += "{:08b}".format(a)[7:]
        # convert the binary string into characters
        str_header = ''.join([chr(int(str_header[i:i + 8], 2)) for i in range(0, len(str_header), 8)])
        str_header = str_header[:str_header.find("/?/?/?/")]
        return str_header.encode()

    def extract_binary_data(self, size, bits, offset):
        str_data = ''
        for y in range(self.height - 5):
            for x in range(self.width):
                if x % int(offset) != 0:
                    continue
                r, g, b, a = self.image.getpixel((x, y))
                str_data += "{:08b}".format(r)[8 - int(bits):]
                str_data += "{:08b}".format(g)[8 - int(bits):]
                str_data += "{:08b}".format(b)[8 - int(bits):]
                str_data += "{:08b}".format(a)[8 - int(bits):]
        str_data = str_data[:size]
        str_data = ''.join([chr(int(str_data[i:i + 8], 2)) for i in range(0, len(str_data), 8)])
        return str_data.encode()

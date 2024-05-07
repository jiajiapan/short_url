import zlib
from dbaccessor import DBAccessor
import logging


class Encoding:
    def __init__(self, settings):
        self.get_db = DBAccessor(settings)

    # Convert the input data to CRC32 value, get the hexadecimal value,
    # and finally get the first seven characters.
    def get_seven_bits(self, input):
        encoded_input = input.encode()
        crc32_value = zlib.crc32(encoded_input)
        hex_value = hex(crc32_value)
        if len(hex_value) > 9:
            seven_bits = hex_value[2:9]
        else:
            seven_bits = hex_value[2:]
        return seven_bits

    # Check whether there is a collision when getting seven bits.
    def check_collision(self, input):
        shorturl = self.get_seven_bits(input)
        longurl = self.get_db.get_longurl(shorturl)
        if longurl and longurl != input:
            return True
        return False

    # Get the final encoding result. If there is no collision, get seven bits.
    # If not, add a character, and get new seven bits as the encoding result.
    def get_encoding(self, input):
        check = self.check_collision(input)
        identifier = "a"
        new_input = input
        while check:
            new_input = new_input + identifier
            logger = logging.getLogger("myapp.log")
            logger.info("new_input:", new_input)
            check = self.check_collision(new_input)
            identifier = chr(ord(identifier) + 1)
        return self.get_seven_bits(new_input)

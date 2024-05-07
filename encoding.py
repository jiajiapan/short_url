import zlib
from dbaccessor import DBAccessor
import logging

logger = logging.getLogger(__name__)


class Encoder:

    def __init__(self, settings):
        self.db_accessor = DBAccessor(settings)

    def get_bits(self, input):
        """
        Convert the input data to CRC32 value, get the hexadecimal value,
        and finally get the first seven characters.
        """
        encoded_input = input.encode()
        crc32_value = zlib.crc32(encoded_input)
        hex_value = hex(crc32_value)
        if len(hex_value) > 9:
            seven_bits = hex_value[2:9]
        else:
            seven_bits = hex_value[2:]
        return seven_bits

    def check_collision(self, long_url, short_url):
        """
        Check whether there is a collision given long_url and corresponding short_url.
        """
        if self.db_accessor.longurl_exists(long_url):
            if self.db_accessor.get_shorturl(long_url) == short_url:
                return False
            return True
        if self.db_accessor.shorturl_exists(short_url):
            if self.db_accessor.get_longurl(short_url) == long_url:
                return False
            return True
        return False

    def get_encoding(self, input):
        """
        Get the final encoding result. If there is no collision, get seven bits.
        If not, add a character, and get new seven bits as the encoding result.
        """
        short_url = self.get_bits(input)
        check = self.check_collision(input, short_url)
        identifier = "a"
        new_input = input
        while check:
            new_input = new_input + identifier
            logger.info("new_input:", new_input)
            short_url = self.get_bits(new_input)
            check = self.check_collision(new_input, short_url)
            identifier = chr(ord(identifier) + 1)
        return short_url

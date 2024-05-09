import zlib
from app.dbaccessor import DBAccessor
import logging

logger = logging.getLogger(__name__)


class Encoder:

    def __init__(self, db_accessor_input):
        self.db_accessor = db_accessor_input

    def get_bits(self, data):
        """
        Convert the input data to CRC32 value, get the hexadecimal value,
        and finally get the first seven characters.
        """
        encoded_data = data.encode()
        crc32_value = zlib.crc32(encoded_data)
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

    def get_encoding(self, data):
        """
        Get the final encoding result. If there is no collision, get seven bits.
        If not, add a character, and get new seven bits as the encoding result.
        """
        short_url = self.get_bits(data)
        check = self.check_collision(data, short_url)
        identifier = "a"
        new_data = data
        while check:
            new_data = new_data + identifier
            logger.info("new_input:", new_data)
            short_url = self.get_bits(new_data)
            check = self.check_collision(new_data, short_url)
            identifier = chr(ord(identifier) + 1)
        return short_url

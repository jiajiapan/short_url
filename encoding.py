import zlib
from dbaccessor import DBAccessor


class encoding:
    def hashing(input):
        crc32_value = zlib.crc32(input.encode())
        shorturl = hex(crc32_value)[:7]
        return shorturl

    def check_collision(input):
        shorturl = encoding.hashing(input)
        get_db = DBAccessor()
        return get_db.shorturl_exists(shorturl)

    def encode(input):
        check = encoding.check_collision(input)
        identifier = "a"
        new_input = input
        while check:
            new_input = new_input + identifier
            check = encoding.check_collision(new_input)
            identifier += 1
        return encoding.hashing(new_input)

import psycopg2
from psycopg2.extras import RealDictCursor
import logging


class DBAccessor:

    def __init__(self, settings):
        self.conn = psycopg2.connect(
            host=settings.database_host,
            database=settings.database_name,
            user=settings.database_user,
            password=settings.database_password,
            cursor_factory=RealDictCursor,
        )

    def longurl_exists(self, long_url):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM url WHERE longurl = (%s)""", (long_url,))
        res = cursor.fetchone()
        count = res["count"]
        logger = logging.getLogger("myapp.log")
        if not count:
            logger.info("longurl doesn't exist!")
            return False
        else:
            logger.info("longurl exists!")
            return True

    def shorturl_exists(self, short_url):
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT COUNT(*) FROM url WHERE shorturl = (%s)""", (short_url,)
        )
        res = cursor.fetchone()
        count = res["count"]
        print("count = ", count)
        if not count:
            print("shorturl doesn't exist!")
            return False
        else:
            print("shorturl exists!")
            return True

    def insert_url_data(self, long_url, short_url):
        cursor = self.conn.cursor()
        if not self.longurl_exists(long_url):
            cursor.execute(
                """INSERT INTO url (longurl, shorturl) VALUES (%s, %s)""",
                (long_url, short_url),
            )
            self.conn.commit()
            self.conn.close()
            print("Data inserted successfully.")

    def get_longurl(self, short_url):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM url WHERE shorturl = (%s)""", (short_url,))
        res = cursor.fetchone()
        if res:
            return res["longurl"]
        return None

import psycopg2
from psycopg2.extras import RealDictCursor
import logging


class DBAccessor:

    # Connect the database, all the settings are defined in config.py and .env.
    def __init__(self, settings):
        self.conn = psycopg2.connect(
            host=settings.database_host,
            database=settings.database_name,
            user=settings.database_user,
            password=settings.database_password,
            cursor_factory=RealDictCursor,
        )

    # Check whether this longurl exists in the database.
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

    # Check whether this shorturl exists in the database.
    def shorturl_exists(self, short_url):
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT COUNT(*) FROM url WHERE shorturl = (%s)""", (short_url,)
        )
        res = cursor.fetchone()
        count = res["count"]
        logger = logging.getLogger("myapp.log")

        if not count:
            logger.info("shorturl doesn't exist!")
            return False
        else:
            logger.info("shorturl exists!")
            return True

    # Insert the coupling data: longurl and shorturl.
    def insert_url_data(self, long_url, short_url):
        cursor = self.conn.cursor()
        if not self.longurl_exists(long_url):
            cursor.execute(
                """INSERT INTO url (longurl, shorturl) VALUES (%s, %s)""",
                (long_url, short_url),
            )
            self.conn.commit()
            self.conn.close()
            logger = logging.getLogger("myapp.log")
            logger.info("Data inserted successfully.")

    # Given a shorturl, find the corresponding longurl in the database.
    def get_longurl(self, short_url):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM url WHERE shorturl = (%s)""", (short_url,))
        res = cursor.fetchone()
        if res:
            return res["longurl"]
        return None

import psycopg2
from psycopg2.extras import RealDictCursor

class dbaccessor:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="mydatabase",
            user="myuser",
            password="mypassword",
            cursor_factory=RealDictCursor,
        )
    
    def insert(self, long_url, short_url):
        cursor = self.conn.cursor
        cursor.execute("""SELECT COUNT(*) FROM url WHERE longurl = %s""", long_url)
        count = cursor.fetchone()
        if not count:
            cursor.execute("""INSERT INTO url (longurl, shorturl) VALUES (%s, %s)""",(long_url,short_url))
        return
    
    def redirect(self,short_url):
        cursor = self.conn.cursor
        cursor.execute("""SELECT * FROM url WHERE shorturl = %s""", short_url)
        res = cursor.fetchone()
        if res:
            return res['longurl']
        return None
    


import psycopg2
from .settings import DB_NAME, USER


class Connector:
    def __init__(self):
        self.name = DB_NAME
        self.user = USER
        self.conn = psycopg2.connect("dbname={} user={}".format(
                                            self.name, self.user))
        self.cursor = self.conn.cursor()

    def execute_query(self, query, values):
        self.cursor.execute(query, values)
        self.conn.commit()

    def execute(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get(self, query, id):
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

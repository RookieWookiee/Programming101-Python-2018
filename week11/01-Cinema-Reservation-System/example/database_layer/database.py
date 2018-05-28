import psycopg2

from .queries import (CREATE_USER_TABLE,
                      CREATE_MOVIES_TABLE,
                      CREATE_PROJECTIONS_TABLE,
                      CREATE_RESERVATION_TABLE)
from .connector import Connector


class DBConnector:
    def __init__(self):
        self.connector = Connector()

    def create(self):
        tables = [CREATE_USER_TABLE, CREATE_MOVIES_TABLE,
                  CREATE_PROJECTIONS_TABLE, CREATE_RESERVATION_TABLE]

        for table in tables:
            self.connector.execute_query(table)

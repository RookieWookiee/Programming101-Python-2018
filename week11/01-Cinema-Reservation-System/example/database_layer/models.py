from .connector import Connector
from .queries import CREATE_MOVIE, LIST_MOVIES


class MovieModel:
    def __init__(self):
        self.conn = Connector()

    def create(self, name, rating):
        query = CREATE_MOVIE
        self.conn.execute_query(query, (name, rating))

    def list(self):
        query = LIST_MOVIES
        return self.conn.all(query)

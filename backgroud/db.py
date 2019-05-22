import pymysql
from collections import deque


class DbSystem(object):
    @staticmethod
    def create_connect() -> pymysql.Connection:
        return pymysql.connect("localhost", 'osa', '123456osa', 'super_oa')

    def __init__(self, size=10):
        self._pool = deque()
        for i in range(size):
            self._pool.append(self.create_connect())

    def get_cursor(self) -> pymysql.Connection:
        if len(self._pool) != 0:
            return self._pool.popleft().cursor()
        else:
            return self.create_connect().cursor()

    def push_back_cursor(self, cursor):
        conn = cursor.connection
        conn.commit()
        self._pool.append(conn)
        while len(self._pool) > 100:
            self._pool.popleft().close()

    def get_read_only_cursor(self) -> pymysql.Connection:
        if len(self._pool) == 0:
            self._pool.append(self.create_connect())
        return self._pool[0].cursor()

import pymysql
from collections import deque


class DbSystem(object):
    @staticmethod
    def create_connect() -> pymysql.Connection:
        return pymysql.connect("localhost", 'osa', '123456osa', 'super_oa')

    def __init__(self, size=10):
        # self._pool = deque()
        # for i in range(size):
            # self._pool.append(self.create_connect())
        pass

    def get_cursor(self) -> pymysql.Connection:
        # if len(self._pool) != 0:
        #     conn = self._pool.popleft()
        #     try:
        #         conn.ping()
        #     except:
        #         conn.close()
        #         conn = self.create_connect()
        #     return conn.cursor()
        # else:
        #     return self.create_connect().cursor()
        return self.create_connect().cursor()

    def push_back_cursor(self, cursor):
        conn = cursor.connection
        conn.commit()
        # self._pool.appendleft(conn)
        # while len(self._pool) > 100:
        #     self._pool.popleft().close()
        conn.close()

    def get_read_only_cursor(self) -> pymysql.Connection:
        # if len(self._pool) == 0:
        #     self._pool.append(self.create_connect())
        # try:
        #     self._pool[0].ping()
        # except:
        #     print('error')
        #     self._pool.popleft().close()
        #     self._pool.appendleft(self.create_connect())
        # return self._pool.popleft().cursor()
        return self.get_cursor()

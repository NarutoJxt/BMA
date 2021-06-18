import psycopg2

from spider import settings
from spider.settings import DATABASE

class PostgreSql:

    def __init__(self,database_config):
        self.database_config = database_config
        self.conn = psycopg2.connect(**self.database_config)
    # get all data
    def pg_query_data(self,sql,params=[]):
        res = []
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            res = cursor.fetchall()
        return res

    def close(self):
        self.conn.close()

    def pg_insert_data(self,sql,params=[]):
        """
           :param sql: str sql sentence
           :param params: the params of sql executed
           :return: 0 insert data false / >=1 success
           """
        cursor = None
        res = None
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        try:
            res = cursor.fetchOne()[0]
        except AttributeError as e:
            res = cursor.rowcount
        finally:
            cursor.close()
            self.conn.commit()
        return res
    def pg_update_data(self,sql,params):
        """
           :param sql: str sql sentence
           :param params: the params of sql executed
           :return: 0 update data false / >=1 success
           """

        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        res = cursor.rowcount
        self.conn.commit()
        cursor.close()
        return res

    def pg_delete_data(self,sql,params):
        """
        :param sql: str sql sentence
        :param params: the params of sql executed
        :return: 0 delete data false / >=1 success
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        res = cursor.rowcount
        self.conn.commit()
        cursor.close()
        return res

pg = PostgreSql(database_config=settings.DATABASE)
sql = """
         insert into tests(a)
         values(%s)
         """
res = pg.pg_insert_data(sql,params=["dasfasf"])
print(res)
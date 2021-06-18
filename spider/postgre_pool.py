import datetime
import sys
import os
import configparser
import logging
import psycopg2

from dbutils.pooled_db import PooledDB


class DatabaseOperator(object):
    '''class for database operator
    '''

    def __init__(self, database_config_path, database_config=None):
        '''Constructor
        '''
        self._database_config_path = database_config_path
        # load database configuration
        if not database_config:
            self._database_config = self.parse_postgresql_config(database_config_path)
        else:
            self._database_config = database_config
        self._pool = None

    def database_config_empty(self):
        if self._database_config:
            return False
        else:
            return True

    def parse_postgresql_config(self, database_config_path=None):
        '''解析数据库配置文件参数
        database_config_path: 数据库配置文件路径
        --------
        返回值: 解析配置属性, 以 dict 类型返回数据库配置参数 config
        '''
        if database_config_path == None and self._database_config_path != None:
            database_config_path = self._database_config_path
        if not os.path.isfile(database_config_path):
            sys.exit("ERROR: Could not find configuration file: {0}".format(database_config_path))
        parser = configparser.SafeConfigParser()
        parser.read(database_config_path)
        config = {}
        config['database'] = parser.get('testdb', 'Database')
        config['db_user'] = parser.get('testdb', 'UserName')
        config['db_passwd'] = parser.get('testdb', 'Password')
        config['db_port'] = parser.getint('testdb', 'Port')
        config['db_host'] = parser.get('testdb', 'Servername')
        self._database_config = config
        return config

    def get_pool_conn(self):
        if not self._pool:
            self.init_pgsql_pool()
        return self._pool.connection()

    def init_pgsql_pool(self):
        '''初始化连接池
        '''
        # 字典 config 是否为空
        config = self.parse_postgresql_config()
        POSTGREIP = config['db_host']
        POSTGREPORT = config['db_port']
        POSTGREDB = config['database']
        POSTGREUSER = config['db_user']
        POSTGREPASSWD = config['db_passwd']
        try:
            logging.info('Begin to create {0} postgresql pool on：{1}.\n'.format(POSTGREIP, datetime.datetime.now()))
            pool = PooledDB(
                creator=psycopg2,  # 使用连接数据库的模块 psycopg2
                maxconnections=6,  # 连接池允许的最大连接数，0 和 None 表示不限制连接数
                mincached=1,  # 初始化时，链接池中至少创建的空闲的链接，0 表示不创建
                maxcached=4,  # 链接池中最多闲置的链接，0 和 None 不限制
                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage=None,  # 一个链接最多被重复使用的次数，None 表示无限制
                setsession=[],  # 开始会话前执行的命令列表
                host=POSTGREIP,
                port=POSTGREPORT,
                user=POSTGREUSER,
                password=POSTGREPASSWD,
                database=POSTGREDB)
            self._pool = pool
            logging.info(
                'SUCCESS: create {0} postgresql pool success on {1}.\n'.format(POSTGREIP, datetime.datetime.now()))

        except Exception as e:
            logging.error(
                'ERROR: create {0} postgresql pool failed on {1}.\n'.format(POSTGREIP, datetime.datetime.now()))
            self.close_db_cursor()
            sys.exit('ERROR: create postgresql pool error caused by {0}'.format(str(e)))

    def pg_select_operator(self, sql):
        '''进行查询操作,函数返回前关闭 cursor, conn
        '''
        # 执行查询
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            logging.error('ERROR: execute {0} causes error'.format(sql))
            sys.exit('ERROR: load data from database error caused {0}'.format(str(e)))
        finally:
            cursor.close()
            conn.close()
        return result

    def exec_sql(self, sql):
        result = False
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            result = True
        except Exception as e:
            logging.error('ERROR: execute  {0} causes error'.format(sql))
            sys.exit('ERROR: insert data from database error caused {0}'.format(str(e)))
        finally:
            cursor.close()
            conn.commit()
            conn.close()
        return result

    def pg_update_operator(self, sql):
        result = False
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            result = True
        except Exception as e:
            logging.error('ERROR: execute  {0} causes error'.format(sql))
            sys.exit('ERROR: update data from database error caused {0}'.format(str(e)))
        finally:
            cursor.close()
            conn.commit()
            conn.close()
        return result
    def pg_insert_oprator(self,sql,params):
        pass
    def pg_delete_operator(self, sql):
        result = False
        # 执行查询
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            result = True
        except Exception as e:
            logging.error('ERROR: execute  {0} causes error'.format(sql))
            sys.exit('ERROR: delete data from database error caused {0}'.format(str(e)))
        finally:
            cursor.close()
            conn.commit()
            conn.close()
        return result

    def close_pool(self):
        '''关闭 pool
        '''
        if self._pool != None:
            self._pool.close()

    def test_pool_select(self):
        sql = 'select * from student'
        result = self.pg_select_operator(sql)
        print(result)

    def test_pool_exec(self, sqlscript):
        result = self.exec_sql(sqlscript)
        print(result)
        return result
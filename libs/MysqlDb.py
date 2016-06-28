# -*- coding: utf-8 -*-
# __author__ = xutao

# Mysql 处理类
import MySQLdb


class MysqlDbUtil(object):

    def __init__(self, host, username, password, database):
        self.db = MySQLdb.connect(host, username, password, database)
        if self.db:
            # 返回值为json结构,好格式化
            self.db.cursorclass = MySQLdb.cursors.DictCursor
        self.cursor = self.db.cursor()

    def all(self, table):
        """
            查询 table 所有数据
        :param table:
        :return:
        """
        sql = "select * from %s" % table
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select(self, table, params=""):
        """
            table name , params 查询字典
        :param table:
        :param params:
        :return:
        """
        if not params:
            # 查询全部
            return self.all(table=table)
        params = params.split("=")
        sql = "select * from %s where %s = '%s'" % (table, params[0], params[1])
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def one(self, table, params=""):
        """
            返回数据集的第一个
        :return:
        """
        if not params:
            return self.all()

        sql = "select * from %s where %s" % (table, params)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def update(self, table, key, value, params):
        """
            更新指定的表
        :param table:
        :param params:
        :return:
        """
        params = params.split("=")
        try:
            value = int(value)
            sql = u"UPDATE %s SET %s = %s where %s = %s" % (table, key, value, params[0], params[1])
        except ValueError, e:
            sql = u"UPDATE %s SET %s = '%s' where %s = %s" % (table, key, value, params[0], params[1])
        try:
            self.cursor.execute(sql)
            return True
        except Exception as e:
            return False

    def select_field_is_not_null(self, table, key):
        """
            筛选字段不为空的
        :param key:
        :return:
        """
        try:
            sql = "select * from %s where %s is not NULL" % (table, key)
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            return False

    def all_order_by(self, table, key, order_key):
        """
            table name ,key value
        :param table:
        :param params:
        :return:
        """
        sql = "select * from %s order by %s %s" % (table, key, order_key)
        self.cursor.execute(sql)
        return self.cursor.fetchall()




import MySQLdb
from collections import Iterable
import os


class MysqlSearch(object):
    conn = None

    def __init__(self):
        self.get_conn()

    # 获取数据库连接
    def get_conn(self):
        try:
            self.conn = MySQLdb.connect(
                host='127.0.0.1',
                user='root',
                passwd='123456',
                port=3306,
                db="news",
                charset='utf8',
                connect_timeout=3
            )
        except MySQLdb.Error as e:
            print('Error: %s' % e)

    # 关闭数据库连接
    def close_conn(self):
        try:
            if self.conn:
                self.conn.close()
        except MySQLdb.Error as e:
            print('Error: %s' % e)

    # 获取一条数据
    def get_one(self):
        sql = "select * from `news` where types = %s order by created_at desc"
        cursor = self.conn.cursor()
        cursor.execute(sql, ('百家',))
        result = dict(zip([k[0] for k in cursor.description], cursor.fetchone()))
        self.close_conn()
        return result

    # 获取多条数据
    def get_more(self, page, page_size):
        offset = (page - 1) * page_size
        sql = 'select * from `news` where types = %s order by created_at desc limit %s,%s'
        cursor = self.conn.cursor()
        cursor.execute(sql, ('百家', offset, page_size))

        result = [dict(zip([k[0] for k in cursor.description], row))
                  for row in cursor.fetchall()]

        return result

    def add_one(self):
        try:
            sql = (
                "insert into `news`(title, image, content, types, is_valid) values"
                "(%s,%s,%s,%s,%s)"
            )
            cursor = self.conn.cursor()
            cursor.execute(sql, ('标题9', '/static/img/news/01.png', '新闻内容', '推荐', 1))
            cursor.execute(sql, ('标题10', '/static/img/news/01.png', '新闻内容', '推荐', '你好'))
            self.conn.commit()
        except:
            print('error')
            print(self.conn)
        finally:
            self.conn.close()
            cursor.close()

def main():
    obj = MysqlSearch()
    # result = obj.get_one()
    # result = obj.get_more(1, 10)
    result = obj.add_one()
    # print(result)


if __name__ == '__main__':
    main()

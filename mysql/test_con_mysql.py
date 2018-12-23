import MySQLdb

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
        result = cursor.fetchone()

        zipObj = zip()

        for v in zipObj:
            print(v)



        self.close_conn()


def main():
    obj = MysqlSearch()
    obj.get_one()


if __name__ == '__main__':
    main()

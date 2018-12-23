import MySQLdb

try:
    conn = MySQLdb.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = '123456',
        port = 3306,
        db = "news",
        charset = 'utf8',
        connect_timeout = 3
    )
    cursor = conn.cursor()
    cursor.execute('select * from news')
    result = cursor.fetchall()

    print(len(result))

except MySQLdb.Error as e:
    print('Error: %s' % e)

conn.close()
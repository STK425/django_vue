import pymysql
from . import my_bean as bean

# 打开数据库连接
db = pymysql.Connect(host = "localhost", port = 3306, user = "root", passwd = "123456", db = "sdu_poas")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def getUserByID(user_id, password):
    try:
        db.ping(reconnect = True)
        sql = "select * from user where user_id = '%s' and password = '%s'"
        data = (user_id, password)
        cursor.execute(sql % data)
        res = cursor.fetchone()
        user = None
        if res:
            user = bean.User(res[0], res[1], res[2], res[3])
        return user
    except BaseException as e:
        print(e)
        return 'error'

def insertUser(user_id, password, type, phone):
    try:
        db.ping(reconnect = True)
        sql = "insert into user values ( '%s', '%s', '%s', '%s')"
        data = (user_id, password, type, phone)
        cursor.execute(sql % data)
        db.commit()
        return 1
    except BaseException as e:
        print(e)
        db.rollback()
        return 0

def getUser():
    try:
        db.ping(reconnect = True)
        sql = "select * from user"
        cursor.execute(sql)
        res = cursor.fetchall()
        users = []
        if res:
            for row in res:
                users.append(bean.User(row[0], row[1], row[2], row[3]))
        return users
    except BaseException as e:
        print(e)
        return 'error'

def deleteUser(user_id):
    try:
        db.ping(reconnect = True)
        sql = "delete from user where user_id = '%s'"
        data = (user_id)
        cursor.execute(sql % data)
        db.commit()
        return 1
    except BaseException as e:
        print(e)
        db.rollback()
        return 0

def getKWInfo(kw):
    try:
        db.ping(reconnect = True)
        sql = "select * from kw where KW = '%s'"
        data = (kw)
        cursor.execute(sql % data)
        res = cursor.fetchone()
        KW = bean.KW(res[0], int(res[1]), int(res[2]), res[3], res[4], res[5], res[6], res[7])
        return KW
    except BaseException as e:
        print(e)
        return None

def getEmotion(source):
    try:
        db.ping(reconnect = True)
        sql = "select * from emotion where source = '%s'"
        data = (source)
        cursor.execute(sql % data)
        res = cursor.fetchone()
        return bean.emotion(res[0], res[1], res[2], res[3])
    except BaseException as e:
        print(e)
        return None

def getEmotionCount(emotion):
    try:
        db.ping(reconnect = True)
        sql = "select count(*) from kw where emotion = %d"
        data = (emotion)
        cursor.execute(sql % data)
        res = cursor.fetchone()
        return int(res[0])
    except BaseException as e:
        print(e)
        return 0

def getKW(kw, pageStart, pageSize):
    try:
        db.ping(reconnect = True)
        sql = "select * from kw where KW like '%s' order by times desc LIMIT %d, %d"
        data = (kw, pageStart, pageSize)
        cursor.execute(sql % data)
        res = cursor.fetchall()
        KWs = []
        if res:
            for row in res:
                KWs.append(bean.KW(row[0], int(row[1]), int(row[2]), row[3], row[4], row[5], row[6], row[7]))
        return KWs
    except BaseException as e:
        print(e)
        return 'error'

def getKWCount(kw):
    try:
        db.ping(reconnect = True)
        sql = "select count(*) from kw where KW like '%s'"
        data = (kw)
        cursor.execute(sql % data)
        res = cursor.fetchone()
        return int(res[0])
    except BaseException as e:
        print(e)
        return -1

def getKWInfo1(limit):
    try:
        db.ping(reconnect = True)
        sql = "select KW,times from kw order by times desc limit %d"
        data = (limit)
        cursor.execute(sql % data)
        res = cursor.fetchall()
        KWs = []
        if res:
            for row in res:
                KWs.append(bean.KW(row[0], int(row[1]), '', '', '', '', ''))
        return KWs
    except BaseException as e:
        print(e)
        return 'error'

def deleteKW(kw):
    try:
        db.ping(reconnect = True)
        sql = "delete from kw where KW = '%s'"
        data = (kw)
        cursor.execute(sql % data)
        db.commit()
        return 1
    except BaseException as e:
        print(e)
        db.rollback()
        return 0

def addKW(KW, times, emotion, days, months, years, sources, otherKW):
    try:
        db.ping(reconnect = True)
        sql = "insert ignore into kw values ('%s', %d, %d, '%s', '%s', '%s', '%s', '%s')"
        data = (KW, times, emotion, days, months, years, sources, otherKW)
        cursor.execute(sql % data)
        db.commit()
        return 1
    except BaseException as e:
        print(e)
        db.rollback()
        return 0

def getLianjie(title, timestamp, source, pageStart, pageSize):
    try:
        db.ping(reconnect = True)
        sql = "select * from data1 where title like '%s' and timestamp like '%s' and source like '%s' " +\
            "order by timestamp desc LIMIT %d, %d"
        data = (title, timestamp, source, pageStart, pageSize)
        cursor.execute(sql % data)
        res = cursor.fetchall()
        LianJie = []
        if res:
            for row in res:
                LianJie.append(bean.lianjie(row[0], row[1], row[2], row[3]))
        return LianJie
    except BaseException as e:
        print(e)
        return 'error'

def getLianjieCount(title, timestamp, source):
    try:
        db.ping(reconnect = True)
        sql = "select count(*) from data1 where title like '%s' and timestamp like '%s' and source like '%s'"
        data = (title, timestamp, source)
        cursor.execute(sql % data)
        res = cursor.fetchone()
        return int(res[0])
    except BaseException as e:
        print(e)
        return 'error'

def getTongji(limit):
    try:
        db.ping(reconnect = True)
        sql = "select source as name, count(*)as value from data1 group by source order by value desc LIMIT %d"
        data = (limit)
        cursor.execute(sql % data)
        res = cursor.fetchall()
        TongJi = []
        if res:
            for row in res:
                TongJi.append(bean.tongji(row[0], int(row[1])))
        return TongJi
    except BaseException as e:
        print(e)
        return 'error'

def deleteLianJie(title):
    try:
        db.ping(reconnect = True)
        sql = "delete from data1 where title = '%s'"
        data = (title)
        cursor.execute(sql % data)
        db.commit()
        return 1
    except BaseException as e:
        print(e)
        db.rollback()
        return 0

def addLianJie(source, timestamp, title, url):
    try:
        db.ping(reconnect = True)
        sql = "insert ignore into data1 values ('%s', '%s', '%s', '%s')"
        data = (source, timestamp, title, url)
        cursor.execute(sql % data)
        db.commit()
        return 1
    except BaseException as e:
        print(e)
        db.rollback()
        return 0

def getUrl():
    try:
        db.ping(reconnect = True)
        sql = "select * from url"
        cursor.execute(sql)
        res = cursor.fetchall()
        list = []
        if res:
            for row in res:
                list.append(row[0])
        return list
    except BaseException as e:
        print(e)
        return 'error'

def deleteUrl(url):
    try:
        db.ping(reconnect = True)
        sql = "delete from url where url = '%s'"
        data = (url)
        cursor.execute(sql % data)
        db.commit()
        return 1
    except BaseException as e:
        print(e)
        db.rollback()
        return 0

def addUrl(url):
    try:
        db.ping(reconnect = True)
        sql = "insert into url values ('%s')"
        data = (url)
        cursor.execute(sql % data)
        db.commit()
        return 1
    except BaseException as e:
        print(e)
        db.rollback()
        return 0


# 关闭数据库连接
db.close()

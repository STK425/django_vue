import pymysql
from . import MyNLP

# 打开数据库连接
db = pymysql.Connect(host = "localhost", port = 3306, user = "root", passwd = "123456", db = "sdu_poas")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

def set_data(list):
    try:
        db.ping(reconnect=True)
        for item in list:
            sql = "insert into data1 values ( '%s', '%s', '%s', '%s')"
            data = (item[2] , item[3], item[0], item[1])
            cursor.execute(sql % data)
            db.commit()
    except BaseException as e:
        print(e)


def get_data():
    data = []
    try:
        db.ping(reconnect = True)
        sql = "select * from data1"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            for row in res:
                data.append([row[2], row[3], row[0], row[1]])
    except BaseException as e:
        print(e)

    return data

def set_InfoKW(KW_list):
    try:
        db.ping(reconnect=True)
        sql = "delete from kw"
        cursor.execute(sql)
        db.commit()

        sql = "insert into kw values ( '%s', %d, %d, '%s', '%s', '%s', '%s', '%s' )"
        for item in KW_list:
            data = ()
            for i in item:
                data = data + (i, )
            cursor.execute(sql % data)
            db.commit()
    except BaseException as e:
        print(e)
    
def set_Emotion(list):
    try:
        db.ping(reconnect=True)
        sql = "update emotion set pos = %d, neu = %d, neg = %d where source = '%s'"
        data = (list[0] , list[1], list[2], list[3])
        cursor.execute(sql % data)
        db.commit()
    except BaseException as e:
        print(e)


def get_Emotion():
    data = []
    try:
        db.ping(reconnect = True)
        sql = "select * from emotion"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            for row in res:
                data.append([int(row[1]), int(row[2]), int(row[3]), row[0]])
    except BaseException as e:
        print(e)

    return data






def get_InfoKW(url):
    sql = "select * from InfoKW where url = '%s'"
    data = (url)
    cursor.execute(sql % data)
    res = cursor.fetchall()
    return MyNLP.Info_kw(res[0], res[1], res[2], res[3], res[4].split(","))

def set_User(mail, pw):
    sql = "insert into User values ( '%s', '%s')"
    data = (mail, pw)
    cursor.execute(sql % data)
    connect.commit()
 
def get_User(mail):
    sql = "select pw from User where mail = '%s'"
    data = (mail)
    cursor.execute(sql % data)
    res = cursor.fetchall()
    return res[0]

def init_KW(kw):
    sql = "insert into KW values ( '%s', 0, '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0,0,0,0', '0,0,0,0,0,0,0,0,0,0,0')"
    data = (KW)
    cursor.execute(sql % data)
    connect.commit()

def add_KW(KW, num, days, months, years):
    sql = "select * from KW where kw = '%s'"
    data = (KW)
    cursor.execute(sql % data)
    res = cursor.fetchall()

    num += int(res[1])
    
    day = ""
    temp = res[2].split(',')
    for i in range(0, 31):
        days[i] = int(temp[i])
        day += days[i] + ","
    day = day[:-2]

    month = ""
    temp = res[3].split(',')
    for i in range(0, 13):
        months[i] = int(temp[i])
        month += months[i] + ','
    month = month[:-2]

    year = ""
    temp = res[4].split(',')
    for i in range(0, 11):
        years[i] = int(temp[i])
        year += year[i] + ','
    year = year[:-2]

    sql = "update KW set num = '%d', days = '%s', months = '%s', years = '%s' where kw = '%s')"
    data = (num, day, month, year, KW)
    cursor.execute(sql % data)
    connect.commit()

#def maintain_KW():

def get_url():
    sql = "select * from url"
    cursor.execute(sql)
    res = cursor.fetchall()
    url_list = []
    for item in res:
        url_list.append(item)
    return url_list

def sef_url(url):
    sql = "insert into url values ( '%s')"
    data = (url)
    cursor.execute(sql % data)
    connect.commit()

def del_url(url):
    sql = "delete from url where url = '%s'"
    data = (url)
    cursor.execute(sql % data)
    connect.commit()


# 关闭数据库连接
db.close()

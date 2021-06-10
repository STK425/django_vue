import datetime
import pandas as pd

#title, url, source, timestamp

def data_processing(path):
    csv = pd.read_csv(path, sep = ',', usecols = [0 ,1, 2, 3, 4], header = None, encoding = 'utf-8')

    #文本清洗
    for index, row in csv.iterrows():
        for i in range(0, 5):
            if pd.isnull(row[i]):
                csv[i][index] = ''
            csv[i][index] = row[i].replace(',', '，').replace('\n', '')
        csv[2][index] = row[2].replace('?', '')
        csv[3][index] = row[3].replace('?', '')

    #时间处理
    today = datetime.date.today()
    csv_index = 0

    for item in csv[3]:
        string = item

        if '-' in string:
            index = string.find('-')
            if len(string) > 11:
                string = string[index - 4 : index + 6]
            i = string.rindex('-')
            while len(string) > i + 1 and string[i + 1].isalnum():
                i = i + 1
            if len(string) > i + 1:
                string = string[0 : i + 1]
            string = string[0 : 4] + '年' + string[5 :]
            string = string.replace('-', '月')
            string += '日'

        elif '/' in string:
            index = string.find('/')
            if len(string) > 11:
                string = string[index - 4 : index + 6]
            i = string.rindex('/')
            while len(string) > i + 1 and string[i + 1].isalnum():
                i = i + 1
            if len(string) > i + 1:
                string = string[0 : i + 1]
            string = string[0 : 4] + '年' + string[5 :]
            string = string.replace('/', '月')
            string += '日'
            
        elif '年' in string:
            index = string.find('年')
            if len(string) > 11:
                string = string[index - 4 : index + 7]
            i = len(string) - 1
            while not string[i] == '日':
                string = string[0 : i]
                i = i - 1
                if i < 4:
                    string = ''
                    break

        elif '月' in string and '日' in string:
            index1 = string.find('月')
            index2 = string.find('日')
            if index2 - index1 > 0 and index2 - index1 < 3:
                    string = str(temp.year) + '年' + string
            else:
                string =''

        elif '分钟前' in string or '小时前' in string or '今天' in string:
            string = str(today.year) + '年' + str(today.month) + '月' + str(today.day) + '日'

        elif '昨天' in string:
            temp = today - datetime.timedelta(1)
            string = str(temp.year) + '年' + str(temp.month) + '月' + str(temp.day) + '日'

        elif '前天' in string:
            temp = today - datetime.timedelta(2)
            string = str(temp.year) + '年' + str(temp.month) + '月' + str(temp.day) + '日'

        elif '天前' in string:
            index = string.find('天前')
            if string[index - 1] == '0':
                temp = today - datetime.timedelta(10)
                string = str(temp.year) + '年' + str(temp.month) + '月' + str(temp.day) + '日'
            else:
                temp = today - datetime.timedelta(int(string[index - 1]))
                string = str(temp.year) + '年' + str(temp.month) + '月' + str(temp.day) + '日'
        else:
            string = ''

        csv[3][csv_index] = string
        csv_index += 1

    #二级爬取信息处理
    data_all = []
    for index, row in csv.iterrows():
        if not pd.isnull(row[0]):
            temp = [row[0], row[1], row[2], row[3]]
            data_all.append(temp)

        if not pd.isnull(row[4]):
            detail = row[4].split('.')
            for item in detail:
                if item:
                    temp = [item, '', row[2] + '（二级）', '']
                    data_all.append(temp)

    #信息提取
    data = []
    for line in data_all:
        if line[1]:
            data.append(line)
        elif '山东大学' in line[0]:
            data.append(line)

    print(len(data_all))
    return data

def data_processing_zhihu(path):
    csv = pd.read_csv(path, sep = ',', usecols = [0 ,1, 2, 3, 4], header = None, encoding = 'utf-8')

    #文本清洗
    for index, row in csv.iterrows():
        for i in range(0, 5):
            if pd.isnull(row[i]):
                csv[i][index] = ''
            csv[i][index] = row[i].replace(',', '，').replace('\n', '')

    #内容提取
    data = []
    PingLun = []
    for index, row in csv.iterrows():
        temp = [row[0] + '，' + row[3].split('||')[0], row[1], '知乎', '']
        if not temp in data:
            data.append(temp)
            temp2 = row[4][2:].split('||')
            for item in temp2:
                PingLun.append(item)

    return data, PingLun

def data_processing_weibo(path):
    csv = pd.read_csv(path, sep = ',', usecols = [0 ,1, 2, 3, 4], header = None, encoding = 'utf-8')

    #文本清洗
    for index, row in csv.iterrows():
        for i in range(0, 5):
            if pd.isnull(row[i]):
                csv[i][index] = ''
            csv[i][index] = row[i].replace(',', '，').replace('\n', '')

    #内容提取
    data = []
    List0 = []
    PingLun = []
    for index, row in csv.iterrows():
        temp = [row[0].replace('#', ''), row[1], '微博', '']
        if not temp in data:
            data.append(temp)
            List0.append(temp[0])
        temp2 = row[4].split('#')
        for item in temp2:
            string = item.replace(' ', '').replace('\u200b', '')
            if string and not string in List0:
                PingLun.append(string)

    return data, PingLun
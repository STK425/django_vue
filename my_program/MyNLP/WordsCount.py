from . import MyNLP as NLP
import datetime
import os

path = os.path.dirname(os.path.abspath(__file__)) + "\\pkuseg\\"

#加载分词情感倾向词库
f = open(path + "BosonNLP_sentiment_score.txt", 'r', encoding = 'utf-8')
KW_emotion_set = {}
for line in f:
    if len(line) > 2:
        temp = line[:-1].split(' ')
        KW_emotion_set[temp[0]] = temp[1]
f.close()

infoSet = []        #原始信息及分词集
KW_count = {}       #关键词计数集（关键词：出现次数）
wordsSet = {}       #关键词集（关键词：关键词所在的NLP）
word_Info_set = []  #关键词信息集（【关键词、出现次数、情感倾向、7日、12月、10年、来源、相关词】）

#数据集生成
def InfoSet_Comput(data):
    for i in data:
        infoSet.append(NLP.Info_kw(i[1], i[0], i[3], i[2]))

    for i in infoSet:
        for j in i.KW:
            if j in KW_count:
                KW_count[j] += 1
            else:
                KW_count[j] = 1
            if not j in wordsSet.keys():
                wordsSet[j] = []
            wordsSet[j].append(i)

"""
    temp_CountList = sorted(KW_count.items(), key = lambda t : t[1], reverse = True)

    KW_count.clear()
    for item in temp_CountList:
        KW_count[item[0]] = item[1]

#获取总排名前十的热词
def get_TopTenInfo():
    index = 0
    res = {}
    for i in KW_count.items():
        res[i[0]] = i[1]
        index += 1
        if index >= 10:
            break

    return res
"""

#获取某个关键词当天及前7天出现的频度
def get_30DaysInfo(word):
    date = datetime.date.today()
    dic = {}
    for i in range(1, 8):                 #当天的前0到30天
        dic[i] = 0
    set = wordsSet[word]

    for item in set:
        if item.time != None:
            sub = (date.__sub__(item.time.date())).days
            if sub <= 7 and sub >= 1:
                dic[sub] += 1
    return dic

#获取某个关键词当月及前12月出现的频度
def get_12MonthsInfo(word):
    date = datetime.date.today()
    dic = {}
    for i in range(0, 13):                  #当月的前0到12个月
        dic[i] = 0
    set = wordsSet[word]

    for item in set:
        if item.time != None:
            sub = date.month - item.time.date().month + (date.year - item.time.date().year) * 12
            if sub <= 12:
                dic[sub] += 1
    return dic

#获取某个关键词当年及前10年出现的频度
def get_10YearsInfo(word):
    date = datetime.date.today()
    dic = {}
    for i in range(0, 11):                  #当年的前0到10年
        dic[i] = 0
    set = wordsSet[word]

    for item in set:
        if item.time != None:
            sub = date.year - item.time.date().year
            if sub <= 10:
                dic[sub] += 1
    return dic

#获取某个关键词的数据源分布
def get_InfoSource(word):
    dic = {}
    set = wordsSet[word]

    for item in set:
        if dic.get(item.source, -1) == -1:
            dic[item.source] = 1
        else:
            dic[item.source] += 1
    return dic

#获取某个关键词的相关关键词
def get_DependentKW(word):
    dic = {}
    set = wordsSet[word]
    
    for item in set:
        for i in item.KW:
            if i in dic:
                dic[i] += 1
            else:
                dic[i] = 0

    temp_CountList = sorted(dic.items(), key = lambda d : d[1], reverse = True)

    dic.clear()
    for item in temp_CountList:
        dic[item[0]] = item[1]

    dic.pop(word)
    return dic.keys()

#获取某个关键词的情感倾向
def get_KW_emotion(word):
    if word in KW_emotion_set.keys():
        if float(KW_emotion_set[word]) > 0:
            return 1
        else:
            return -1
    return 0


#获取目标表格
def list_to_str(list):
    string = ''
    for i in list:
        string += str(i) + '，'
    return string[:-1]

def get_all():
    for item in wordsSet.items():
        temp = []
        temp.append(item[0])
        temp.append(KW_count[item[0]])
        temp.append(get_KW_emotion(item[0]))
        temp.append(list_to_str(get_30DaysInfo(item[0]).values()))
        temp.append(list_to_str(get_12MonthsInfo(item[0]).values()))
        temp.append(list_to_str(get_10YearsInfo(item[0]).values()))
        temp.append(list_to_str(get_InfoSource(item[0]).keys()))
        temp.append(list_to_str(get_DependentKW(item[0])))

        word_Info_set.append(temp)

    return word_Info_set
    
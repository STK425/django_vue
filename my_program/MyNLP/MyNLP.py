import pkuseg
import datetime
import os

#加载词性标记、字典、停用词词库、无关词词库
tags = ['n', 'v', 'a']#, 'd'
lexicon = []
stopwords = []
irrelevantwords = []

path = os.path.dirname(os.path.abspath(__file__)) + "\\pkuseg\\"
f = open(path + "lexicon.txt", "r", encoding = "utf-8")
for line in f:
    lexicon.append(line[:-1])
f.close()
f = open(path + "stopwords.txt", "r", encoding = "utf-8")
for line in f:
    stopwords.append(line[:-1])
f.close()
f = open(path + "IrrelevantWords.txt", "r", encoding = "utf-8")
for line in f:
    irrelevantwords.append(line[:-1])
f.close()

#加载分词器
seg = pkuseg.pkuseg(model_name = path + "news", user_dict = lexicon, postag = True)

#信息-关键词 结构体
class Info_kw:
    def __init__(self, url, text, time, source, KW = []):
        self.url = url
        self.text = text
        self.source = source
        try:
            if time:
                self.time = datetime.datetime.strptime(time, "%Y年%m月%d日")
            else:
                self.time = None
        except BaseException as e:
            print(e)
            print(time)

        if KW:
            self.KW = KW
        else:
            self.KW = []
            self.NLP()

    def NLP(self):
        #分词
        rsts = seg.cut(self.text)

        #去重，根据词性筛选
        self.temp = []
        for i in rsts:
            if not i[0] in self.temp and i[1] in tags and len(i[0]) > 1 and self.MyFunc(i[0]):
                self.temp.append(i[0])

        #去停用词，去无关词
        for i in self.temp:
            if i not in stopwords and i not in irrelevantwords:
                self.KW.append(i)

    #去除开头末尾为数字或符号的分词，如日期、错误分词（“...样本”）
    def MyFunc(self, str):
        if str[0].isnumeric() or str[-1].isnumeric():
            return False
        stop = '!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+：；￥（）—「'
        if str[0] in stop or str[-1] in stop:
            return False
        return True

    def get_KW_str(self):
        str = ""
        for i in self.KW:
            str += (i + ",")
        str = str[:-2]
        return str
    
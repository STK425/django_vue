from . import data_processing as dp
from . import SQL
from . import WordsCount as wc
from . import emotion as emo
import os

BasicPath = os.path.dirname(os.path.abspath(__file__)) + "\\Spider\\"

Data_path = ['Spider_baidu\\Spider_baidu\\spiders\\baidu.csv',
             'Spider_cctv\\Spider_cctv\\spiders\\cctv.csv',
             'Spider_headline\\Spider_headline\\spiders\\headline.csv',
             'Spider_sina\\Spider_sina\\spiders\\sina.csv',
             'Spider_wangyi\\Spider_wangyi\\spiders\\wangyi.csv',
             'Spider_iqilu\\Spider_iqilu\\spiders\\iqilu.csv']

def main():
    #爬虫爬取
    os.system(BasicPath + 'Spider_baidu\\main.py')
    os.system(BasicPath + 'Spider_cctv\\main.py')
    os.system(BasicPath + 'Spider_headline\\main.py')
    os.system(BasicPath + 'Spider_sina\\main.py')
    os.system(BasicPath + 'Spider_wangyi\\main.py')
    os.system(BasicPath + 'Spider_zhihu\\main.py')
    os.system(BasicPath + 'Spider_weibo\\main.py')
    os.system(BasicPath + 'Spider_iqilu\\main.py')

    #数据获取
    data_list = []

    for path in Data_path:
        temp_list = dp.data_processing(BasicPath + path)
        for item in temp_list:
            data_list.append(item)


    data1, pl1 = dp.data_processing_zhihu(BasicPath + 'Spider_zhihu\\Spider_zhihu\\spiders\\zhihu.csv')
    data2, pl2 = dp.data_processing_weibo(BasicPath + 'Spider_weibo\\Spider_weibo\\spiders\\weibo.csv')


    for item in data1:
        data_list.append(item)
    for item in data2:
        data_list.append(item)

    temp_list = SQL.get_data()
    SQL.set_data(data_list)

    #热词处理
    for item in temp_list:
        data_list.append(item)

    wc.InfoSet_Comput(data_list)
    SQL.set_InfoKW(wc.get_all())


    #评论处理
    emo_list = SQL.get_Emotion()
    zhihu_list = emo.get_emotion(pl1, emo_list[0])
    zhihu_list.append('zhihu')
    weibo_list = emo.get_emotion(pl2, emo_list[1])
    weibo_list.append('weibo')

    SQL.set_Emotion(zhihu_list)
    SQL.set_Emotion(weibo_list)

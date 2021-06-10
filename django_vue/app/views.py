from django.shortcuts import HttpResponse, render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

from my_program import my_bean as bean
from my_program import my_sql as sql
import datetime

from .models import User

from my_program import system

MySys = system.MainSystem()

def register(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        i = sql.insertUser(request_body['user_id'], request_body['password'], request_body['type'], request_body['phone'])
        if i == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("ok")
    except Exception as e:
        print(str(e))
        return HttpResponse("error")

def login(request):
    response = {} 
    try:
        response['flag'] = 'error'
        request_body = json.loads(request.body.decode('utf-8'))
        user = sql.getUserByID(request_body['user_id'], request_body['password'])

        if user:
            response['flag'] = 'ok'

        response['user'] = user.toDist()
            
        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def getUser(request):
    response = {} 
    try:
        user_list = sql.getUser()
        list = []
        for item in user_list:
            list.append(item.toDist())

        response['user_list'] = list
            
        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def deleteUser(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        i = sql.deleteUser(request_body['user_id'])
        if i == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("ok")
    except Exception as e:
        print(str(e))
        return HttpResponse("error")

def getKW(request):
    response = {} 
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        KW_list = sql.getKW('%' + request_body['infoKW'] + '%', int(request_body['pageNum']), int(request_body['pageSize']))

        list = []
        for item in KW_list:
            list.append(item.toDist())

        response['kw_list'] = list

        response['num'] = sql.getKWCount('%' + request_body['infoKW'] + '%')
            
        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def list_int(list):
    res = []
    for item in list:
        res.append(int(item))
    return res

def KWinfo(request):
    response = {} 
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        KW = sql.getKWInfo(request_body['KW'])

        emotion = {1 : '积极', 0 : '中性', -1 : '消极'}

        days_label = []
        today = datetime.date.today()
        for i in range(1, 8):
            mlast_day = today - datetime.timedelta(i)
            days_label.append(mlast_day.strftime('%Y-%m-%d'))

        if KW == None:
            response['flag'] = 'false'
        else:
            response['days'] = list_int(KW.getDays().split('，'))
            response['months'] = list_int(KW.getMonths().split('，'))
            response['years'] = list_int(KW.getYears().split('，'))
            response['times'] = KW.getTimes()
            response['source'] = KW.getSources()
            response['otherKW'] = KW.getOtherKW().split('，')
            response['flag'] = 'true'
            response['emotion'] = emotion[KW.getEmotion()]
            response['days_label'] = days_label

        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def kw_info1(request): 
    response = {} 
    try:
        KW_list = sql.getKWInfo1(10)

        result = []
        label = []
        size = []
        for item in KW_list:
            temp = {}
            temp['name'] = item.getKW()
            temp['value'] = item.getTimes()
            result.append(temp)
            label.append(item.getKW())
            size.append(item.getTimes())

        response['shan'] = result
        response['label'] = label
        response['size'] = size
            
        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def kw_info_source(request):
    response = {} 
    try:
        TJ_list = sql.getTongji(10)
        KW_list = sql.getKWInfo1(10)

        result = []
        label = []
        size = []
        for item in TJ_list:
            temp = {}
            temp['name'] = item.getName()
            temp['value'] = item.getValue()
            result.append(temp)
        for item in KW_list:
            label.append(item.getKW())
            size.append(item.getTimes())

        emotion = [sql.getEmotionCount(-1), sql.getEmotionCount(0), sql.getEmotionCount(1)]

        response['shan'] = result
        response['label'] = label
        response['size'] = size
        response['emotion'] = emotion
            
        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def movie_info(request):
    return HttpResponse("1")

def getemotion(request):
    response = {} 
    try:
        emotion = [sql.getEmotionCount(-1), sql.getEmotionCount(0), sql.getEmotionCount(1)]

        response['emotion'] = emotion
            
        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def getEmotion(request):
    response = {} 
    try:
        weibo = sql.getEmotion("weibo");
        weiboresult = [{'name' : '消极', 'value' : weibo.getNeg()},
                       {'name' : '中性', 'value' : weibo.getNeu()},
                       {'name' : '积极', 'value' : weibo.getPos()}]
        weibosize = [weibo.getNeg(), weibo.getNeu(), weibo.getPos()]

        zhihu = sql.getEmotion("zhihu");
        zhihuresult = [{'name' : '消极', 'value' : zhihu.getNeg()},
                       {'name' : '中性', 'value' : zhihu.getNeu()},
                       {'name' : '积极', 'value' : zhihu.getPos()}]
        zhihusize = [zhihu.getNeg(), zhihu.getNeu(), zhihu.getPos()]

        response['weiboresult'] = weiboresult
        response['weibosize'] = weibosize
        response['zhihuresult'] = zhihuresult
        response['zhihusize'] = zhihusize
            
        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def deleteKW(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        i = sql.deleteKW(request_body['kw'])
        if i == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("ok")
    except Exception as e:
        print(str(e))
        return HttpResponse("error")

def addKW(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        i = sql.deleteKW(request_body['KW'], int(request_body['times']), request_body['days'], request_body['months'], request_body['years'], request_body['sources'], request_body['otherKW'])
        if i == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("ok")
    except Exception as e:
        print(str(e))
        return HttpResponse("error")

def movie(request):
    response = {} 
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        LianJie_list = sql.getLianjie('%' + request_body['KW'] + '%', '%' + request_body['year'] + '%', '%' + request_body['source'] + '%', int(request_body['pageNum']), int(request_body['pageSize']))
        num = sql.getLianjieCount('%' + request_body['KW'] + '%', '%' + request_body['year'] + '%', '%' + request_body['source'] + '%')

        list = []
        for item in LianJie_list:
            list.append(item.toDist())

        response['num'] = num
        response['lianjie_list'] = list

        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def getTongji(request):
    response = {} 
    try:
        TongJi_list = sql.getTongji(10)

        result = []
        label = []
        size = []
        for item in TongJi_list:
            temp = {}
            temp['name'] = item.getName()
            temp['value'] = item.getValue()
            result.append(temp)
            label.append(item.getName())
            size.append(item.getValue())

        response['shan'] = result
        response['label'] = label
        response['size'] = size
            
        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def deleteLianJie(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        i = sql.deleteLianJie(request_body['title'])
        if i == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("ok")
    except Exception as e:
        print(str(e))
        return HttpResponse("error")

def addLianJie(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        i = sql.addLianJie(request_body['source'], request_body['timestamp'], request_body['title'], request_body['url'])
        if i == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("ok")
    except Exception as e:
        print(str(e))
        return HttpResponse("error")

def getUrl(request):
    response = {} 
    try:
        Url_list = sql.getUrl()
        response['url_list'] = Url_list
            
        response['msg'] = 'success'
        response['error_num'] = 0
    except BaseException as e:
        print(e)
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def deleteUrl(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        i = sql.deleteUrl(request_body['url'])
        if i == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("ok")
    except Exception as e:
        print(str(e))
        return HttpResponse("error")

def addUrl(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        i = sql.addUrl(request_body['url'])
        if i == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("ok")
    except Exception as e:
        print(str(e))
        return HttpResponse("error")

def System(request):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
        handle = request_body['handle']

        if handle == 'start':
            if MySys.is_running():
                return HttpResponse("running")
            else:
                MySys.sys_start()
                return HttpResponse("success")
        elif handle == 'start_C':
            flag = MySys.sys_main_start()
            if flag == 0:
                return HttpResponse("running")
            elif flag == 1:
                return HttpResponse("success")
            else:
                return HttpResponse("error")
        else:
            if MySys.sys_main_is_running():
                return HttpResponse("running")
            else:
                MySys.sys_end()
                return HttpResponse("success")

    except Exception as e:
        print(str(e))
        return HttpResponse("error")
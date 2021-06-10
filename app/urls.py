from django.conf.urls import include
from django.urls import re_path
from .views import *
 
 
urlpatterns = [
    #user
    re_path(r'Register$', register, ),
    re_path(r'Login$', login, ),
    re_path(r'getuser$', getUser, ),
    re_path(r'shanchuuser$', deleteUser, ),
    #kw
    re_path(r'kw_query$', getKW, ),
    re_path(r'KWinfo$', KWinfo, ),
    re_path(r'kw_info1$', kw_info1, ),
    re_path(r'kw_info_source$', kw_info_source, ),
    re_path(r'KWinfo1$', movie_info, ),
    re_path(r'getemotion$', getemotion, ),
    re_path(r'getEmotion$', getEmotion, ),
    re_path(r'shanchureci$', deleteKW, ),
    re_path(r'addreci$', addKW, ),
    #lianjie
    re_path(r'lianjie_query$', movie, ),
    re_path(r'getTongji$', getTongji, ),
    re_path(r'shanchulianjie$', deleteLianJie, ),
    re_path(r'addlianjie$', addLianJie, ),
    #url
    re_path(r'geturl$', getUrl, ),
    re_path(r'shanchuurl$', deleteUrl, ),
    re_path(r'tianjiaurl$', addUrl, ),
    #system
    re_path(r'system$', System, ),
]





#package com.example.demo.bean

class KW:
    def __init__(self, KW = '', times = 0, emotion = 0, days = '', months = '', years = '', sources = '', otherKW = ''):
        self.KW = KW
        self.times = times
        self.emotion = emotion
        self.days = days
        self.months = months
        self.years = years
        self.sources = sources
        self.otherKW = otherKW

    def getKW(self):
        return self.KW

    def setKW(self, kw):
        self.KW = kw

    def getTimes(self):
        return self.times
    
    def setEmotion(self, emotion):
        self.emotion = emotion

    def getEmotion(self):
        return self.emotion
    
    def setTimes(self, times):
        self.times = times
    
    def getDays(self):
        return self.days
   
    def setDays(self, days):
        self.days = days
    
    def getMonths(self):
        return self.months
    
    def setMonths(self, months):
        self.months = months
    
    def getYears(self):
        return self.years
    
    def setYears(self, years):
        self.years = years
    
    def getSources(self):
        return self.sources
    
    def setSources(self, sources):
        self.sources = sources
    
    def getOtherKW(self):
        return self.otherKW
    
    def setOtherKW(self, otherKW):
        self.otherKW = otherKW
    
    #@Override
    def toString(self):
        return "KW{" +\
            "KW='" + self.KW + '\'' +\
            ", times='" + self.times + '\'' +\
            ", emotion='" + self.emotion + '\'' +\
            ", days='" + self.days + '\'' +\
            ", months='" + self.months + '\'' +\
            ", years='" + self.years + '\'' +\
            ", sources='" + self.sources + '\'' +\
            ", otherKW='" + self.otherKW + '\'' +\
            '}'
    
    def toDist(self):
        return {'kW' : self.KW,
                'times' : self.times,
                'emotion' : self.emotion,
                'days' : self.days,
                'months' : self.months,
                'years' : self.years,
                'source' : self.sources,
                'otherKW' : self.otherKW
                }
    


class lianjie:
    def __init__(self, sources = '', timestamp = '', title = '', url = ''):
        self.title = title
        self.timestamp = timestamp
        self.sources = sources
        self.url = url

    def getTitle(self):
        return self.title
    
    def setTitle(self, title):
        self.title = title
    
    def getTimestamp(self):
        return self.timestamp
    
    def setTimestamp(self, timestamp):
        self.timestamp = timestamp
    
    def getSource(self):
        return self.source

    def setSource(self, source):
        self.source = source
    
    def getUrl(self):
        return self.url
    
    def setUrl(self, url):
        self.url = url
    
    #@Override
    def toString(self):
        return "lianjie{" +\
            "title='" + self.title + '\'' +\
            ", timestamp='" + self.timestamp + '\'' +\
            ", sources='" + self.sources + '\'' +\
            ", url='" + self.url + '\'' +\
            ''
    
    def toDist(self):
        return {'title' : self.title,
                'timestamp' : self.timestamp,
                'source' : self.sources,
                'url' : self.url,
                }



class tongji:
    def __init__(self, name = '', value = 0):
        self.name = name
        self.value = value

    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
    #@Override
    def toString(self):
        return "tongji{" +\
            "name='" + self.name + '\'' +\
            ", value=" + self.value +\
            '}'
    
    def toDist(self):
        return {'name' : self.name,
                'value' : self.value,
                }



class User:
    def __init__(self, user_id = '', password = '', type = '', phone = ''):
        self.user_id = user_id
        self.password = password
        self.type = type
        self.phone = phone

    def getUser_id(self):
        return self.user_id

    def setUser_id(self, user_id):
        self.user_id = user_id

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getPhone(self):
        return self.phone

    def setPhone(self, phone):
        self.phone = phone

    #@Override
    def toString(self):
        return "User{" +\
            "user_id='" + self.user_id + '\'' +\
            ",password='" + self.password + '\'' +\
            ",type='" + self.type + '\'' + \
            ",phone='" + self.phone + '\'' +\
            '}'

    def toDist(self):
        return {'user_id' : self.user_id,
                'password' : self.password,
                'type' : self.type,
                'phone' : self.phone,
                }

class emotion():
    def __init__(self, source = '', pos = 0, neu = 0, neg = 0):
        self.source = source
        self.pos = pos
        self.neu = neu
        self.neg = neg

    def getSource(self):
        return self.source

    def setSource(self, source):
        self.source = source

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def getNeu(self):
        return self.neu

    def setNeu(self, neu):
        self.neu = neu

    def getNeg(self):
        return self.neg

    def setNeg(self, neg):
        self.neg = neg

    def toString(self):
        return "emotion{" \
            "source='" + self.source + '\'' \
            ", pos=" + self.pos + '\'' \
            ", neu=" + self.neu + '\'' \
            ", neg=" + self.neg + '\'' \
            '}'
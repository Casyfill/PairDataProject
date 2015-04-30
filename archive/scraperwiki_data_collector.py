#!/usr/bin/env python
# -*- coding: utf-8 -*-

#! начать сборы                   - done
#! parse transport                - done
#! сделать сбор за вчера          - done
#! сделать парс мест              - semidone 
#! сделать получение типа места   - !
#! завернуть val в функцию
#! сделать общую функцию
#! считать 


#! обратное геокодирование curl "http://www.datasciencetoolkit.org/coordinates2politics/37.769456%2c-122.429128"
#! оценивать разнообразиве мест
#! расчитовать времяпроведение для каждого места

#! Визуализация - тз
#! Визуализация  - вопрос





import scraperwiki
import requests
#import datetime
import json 
import time
from datetime import date, timedelta

yesterday = date.today() - timedelta(1)
yesterdayString = yesterday.strftime( "%Y, %m, %d" ).replace(', ','')

Pcode = 'Xo7E7yyip4_96_B5f9rq4EZ1yxiXL8LNyEVGsSJ70sChY02JbC_ST4Z2sZff1Hgc'
Ncode = 'hTfMNzVmnyV82f9UHpH1P5_mE9XQy4TzO2ECg2q78S337K1mYQrCuOthOKXj1t01'


clientId = 'F4osaamCVlvuJ6c2FHWb179BGUr7vr5Q'
clientSecret = 'Dvm4tKTuRmV3efrl6KKhDritiLNp80k5f5BvRF65c7grV7OPWcnZc1N825agj4Ul'
redirect = 'http://cargocollective.com/Cityfish'

#{"access_token":"J1ojw80T9QCmx7kAX90H54OeVfY9n9xs8hOLYyGvgp39vS05O7F8aKe76PBiaTt_","token_type":"bearer","expires_in":15551999,"refresh_token":"d571v6g1lbdOov2l73velNT8OLn_y90hN77S7hxksgbyF459Aw5JY1WLjTM6gt10","user_id":7871067748186666}

PacessToken = 'lmRD9Sd291uQ1NfsFatZrJ9zYs1Oji2nlr1Il6vd8vbKGUATWq_H91r626wbZfOf'
NacessToken='kEdGCM2pYZwIT7I4GsVkx2crGu54ImhQIFZ2y2r47QLi4pr7BVpTGvraPzF5fCiS'


def getAcess(code,clientId ,clientSecret , redirect):
    p = 'https://api.moves-app.com/oauth/v1/access_token?grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=%s' % (code,clientId ,clientSecret , redirect)

    r = requests.post(p)
    return r

    #undone
    #print r.text
    #print r.access_token

    #acessToken = r.access_token
    #expiresIn = r.expires_in
    #refreshToken = r.refresh_token
    #userID = r.user_id


#x = getAcess(Ncode,clientId ,clientSecret , redirect)
#print x.content

def refresh(refreshToken, clientId ,clientSecret):
    refrURL = 'https://api.moves-app.com/oauth/v1/access_token?grant_type=refresh_token&refresh_token=%s&client_id=%s&client_secret=%s' % (refreshToken, clientId ,clientSecret)
    rRefresh = requests.post(refrURL)

    # undone
    #acessToken = r.access_token
    #expiresIn = r.expires_in
    #refreshToken = r.refresh_token
    #userID = r.user_id
    
def validate(aT):
    valURL = 'https://api.moves-app.com/oauth/v1/tokeninfo?access_token=%s' % (aT)
    val = requests.get(valURL)
    return val._content

# endpoint defs

def summary(aT, yStr):
    generalURL = 'https://api.moves-app.com/api/v1'
    ac = '?access_token=%s' % (aT)
    toDay = yStr
    
    dailySummary = '/user/summary/daily/%s' % (toDay)
    
    url = generalURL  + dailySummary + ac
    
    result = requests.get(url) 
    return result._content

def story(aT, yStr):
    generalURL = 'https://api.moves-app.com/api/v1'
    ac = '&access_token=%s' % (aT)
    
    toDay = yStr
    
    q = '/user/storyline/daily/%s?trackPoints=true' % (toDay)
    
    url = generalURL  + q + ac
    #print url
    
    result = requests.get(url) 
    return result._content    
    
#functional defs

def parseJsonString (jsonString):
    p = json.loads(jsonString)
    return p







# НАЧАЛИ КОМПУТИНГ


# z = getAcess(Ncode,clientId ,clientSecret , redirect)
# print z.content

# P "access_token":"lmRD9Sd291uQ1NfsFatZrJ9zYs1Oji2nlr1Il6vd8vbKGUATWq_H91r626wbZfOf","token_type":"bearer","expires_in":15551999,"refresh_token":"z9zhOObbm09gyfsWBVHh_JZg70iZ8rA9CYLPF90K55HE84CSnoRi4OR2dQy7xiEq","user_id":7676905336889632}
# N {"access_token":"kEdGCM2pYZwIT7I4GsVkx2crGu54ImhQIFZ2y2r47QLi4pr7BVpTGvraPzF5fCiS","token_type":"bearer","expires_in":15551999,"refresh_token":"ElZ8fHnXEFjCvdIKL9woh584DUM1KRN6NNJO9Y4kOxU9aGhBIUrpv6PRastjID6e","user_id":7871067748186666}

print validate(PacessToken)
print validate(NacessToken)
#scraping

PhilippActivityString = summary(PacessToken, yesterdayString)
PhilippStoryString = story(PacessToken, yesterdayString)

NuraActivityString = summary(NacessToken, yesterdayString)
NuraStoryString = story(NacessToken, yesterdayString)



Pactivities = parseJsonString (PhilippActivityString)
Nactivities = parseJsonString (NuraActivityString)

Pstory = parseJsonString(PhilippStoryString)
Nstory = parseJsonString(NuraStoryString)

Prun = 0 
Pwlk = 0
Pcyc = 0
Ptrs = 0

Nrun = 0 
Nwlk = 0
Ncyc = 0
Ntrs = 0

if Pactivities[0]['summary'] != None:
    for a in Pactivities[0]['summary']:
        aType = a['activity']
        aDist = a['distance']
    
        if aType == 'wlk':
            Pwlk = aDist
        elif aType == 'run':
            Prun = aDist
        elif aType == 'cyc':
            Pcyc = aDist

if Nactivities[0]['summary'] != None:
    for a in Nactivities[0]['summary']:
        aType = a['activity']
        aDist = a['distance']
    
        if aType == 'wlk':
            Nwlk = aDist
        elif aType == 'run':
            Nrun = aDist
        elif aType == 'cyc':
            Ncyc = aDist
        
    

'''
Pplaces = []
PplaceTypes = []
PplacesData = []
Nplaces4sqr = []

Nplaces = []
NplaceTypes = []
NplacesData = []
Nplaces4sqr = []
'''

# parse transportation
Pplaces = "{u'places':{"
Nplaces = "{u'places':{"

PplaceCount = 0
NplaceCount = 0

if Pstory[0]['segments'] !=None: 
    for a in Pstory[0]['segments']:
        if a['type']=='move':
            for b in a['activities']:
                if b['activity'] == 'trp':
                    Ptrs+=int(b['distance'])
        elif a['type']=='place':
        #tempPlace = json.dump(vars(a['type'][0]), sort_keys=True)
        #print str(a)

            Pplaces = Pplaces +' ' + str(a)
            PplaceCount+=1
else:
    Pplases = '{{none'
        
    
Pplaces+='}}'
        

for a in Nstory[0]['segments']:
    if a['type']=='move':
        for b in a['activities']:
            if b['activity'] == 'trp':
                Ntrs+=int(b['distance'])
    elif a['type']=='place':
        Nplaces = Nplaces +' ' + str(a)
        NplaceCount+=1
        
Nplaces+='}}'

Pplaces = ''
Nplaces = ''


print yesterday
print 'run | wlk | кcyc | trs | placeCount | trs | placeCount'
print 'Philipp|', Prun, '|', Pwlk, '|', Pcyc, '|', Ptrs, '|', PplaceCount , '|', Ptrs, '|', PplaceCount
print 'Anna|', Nrun, '|', Nwlk, '|', Ncyc, '|', Ntrs, '|', NplaceCount , '|',  Ntrs, '|',NplaceCount


# Saving data:
unique_keys = [ 'Time' ]
data = {  'Time': yesterday, 'Ptrs':Ptrs, 'Ntrs':Ntrs, 'NplaceCOunt': NplaceCount, 'PplaceCount': PplaceCount, 'Pplaces': Pplaces, 'Nplaces':Nplaces, 'Pcyc': Pcyc, 'Prun': Prun, 'Pwlk': Pwlk, 'Ncyc': Ncyc, 'Nrun': Nrun, 'Nwlk': Nwlk, 'PhilippActivityString': PhilippActivityString.decode('utf-8', 'ignore'), 'PhilippStoryString': PhilippStoryString.decode('utf-8', 'ignore'), 'NuraActivityString': NuraActivityString.decode('utf-8', 'ignore'), 'NuraStoryString': NuraStoryString.decode('utf-8', 'ignore') }

scraperwiki.sql.save(unique_keys, data)






# Check my Expiration

# Pval = validate(PacessToken)
# print Pval
# # PexpiresIn = int(parseJsonString (Pval).get('expires_in'))
# print 'Philipp`s expires in: ', PexpiresIn

# # if PexpiresIn <= 600000:  #если осталось меньше недели

# print 'Alert!'
# x = refresh(PrefreshToken, PclientId , PclientSecret)
# PrefreshData = parseJsonString (x)
    
#     #+ НУЖНО РЕФРЕШ ЗАВЕРНУТЬ В ФУНКЦИЮ
    
# PrefreshToken =PrefreshData.get('refresh_token')
# PacessToken = PrefreshData.get('access_token')
    
    
# Check Anna`s Expiration

# Nval = validate(NacessToken)
# NexpiresIn = int(parseJsonString (Nval).get('expires_in'))
# print 'Nura`s expires in: ', NexpiresIn

# # if NexpiresIn <= 600000:  #если осталось меньше недели

# print 'Alert!'
# y = refresh(NrefreshToken, NclientId , NclientSecret)
# NrefreshData = parseJsonString (y)
    
# NrefreshToken =NrefreshData.get('refresh_token')
# NacessToken = NrefreshData.get('access_token')
    

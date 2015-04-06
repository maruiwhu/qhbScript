# coding=utf-8

import http.client
import urllib
import json
import time
import traceback
from time import sleep
import sys
import _thread

ISOTIMEFORMAT='%Y-%m-%d %X'
lopper = True
headers = {"X-Forwarded-For":"10.0.0.1"}
string = "\t兑奖中!!!!!!!!!!!!!!!!!!!!!!!!"
string1 = "\t总数： "
string2 = "\t总投入："
string3 = "\t每次投入："

def monitor(owenId):
        values = {'sEcho':1,
	'iColumns':7,
	'sColumns':',,,,,,',
	'iDisplayStart':0,
	'iDisplayLength':10,
	'mDataProp_0':0,
	'bRegex_0':'false',
	'bSearchable_0':'true',
	'mDataProp_1':1,
	'bRegex_1':'false',
	'bSearchable_1':'true',
	'mDataProp_2':2,
	'sSearch_2':'',
	'bRegex_2':'false',
	'bSearchable_2':'true',
	'mDataProp_3':3,
	'sSearch_3':'',
	'bRegex_3':'false',
	'bSearchable_3':'true',
	'mDataProp_4':4,
	'sSearch_4':'',
	'bRegex_4':'false',
	'bSearchable_4':'true',
	'mDataProp_5':5,
	'sSearch_5':'',
	'bRegex_5':'false',
	'bSearchable_5':'true',
	'mDataProp_6':6,
	'sSearch_6':'',
	'bRegex_6':'false',
	'bSearchable_6':'true',
	'sSearch':'',
	'bRegex':'false',
	'ownerId':owenId,
	'status':''}
        headers = {'Accept':'application/json, text/javascript, */*; q=0.01','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Host':'qhb.qbao.com','Origin':'http://qhb.qbao.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'}
        data = urllib.parse.urlencode(values)
        httpClient = http.client.HTTPConnection("qhb.qbao.com", timeout=30)
        httpClient.request("POST", "/ajax/listGroup.html", data, headers)
        response = httpClient.getresponse()
        the_page =response.read().decode('utf-8')
        the_page_list = the_page.split("\r\n")
        the_page_now = ""
        if len(the_page_list)==1:
                the_page_now = the_page
        else:
                for i in range(len(the_page_list)):
                        if(i%2 == 1):
                                the_page_now=the_page_now+the_page_list[i]
                the_page_now = the_page_now.replace("\r\n","")
        strResponse = json.loads(the_page_now)
        aaData = strResponse["data"]["aaData"]
        small = 0;
        large = 0;
        for i in range(len(aaData)):
                if aaData[i]["status"] == "CLOSED":
                        if aaData[i]["raffleCount"] >= 250:
                                large += 1
                        elif aaData[i]["raffleCount"] < 250:
                                small += 1
        print('\n' + owenId+" "+"大团" + str(large) + "个---小团" + str(small) + "个")
        if "RAFFING" in str(aaData):
                lopper = False
                print('\n' + time.strftime( ISOTIMEFORMAT, time.localtime() ))
                print('\n' + owenId+ " " + ("大团" if aaData[i]["raffleCount"] > 250 else "小团") + " " +string)
        _thread.exit_thread()
        
def qhbCount(num):
        global lastCount
        global firstCount
        params = urllib.parse.urlencode({'ie': 'utf-8'})
        headers = {'Accept':'application/json, text/javascript, */*; q=0.01','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Host':'qhb.qbao.com','Origin':'http://qhb.qbao.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'}
        httpClient = http.client.HTTPConnection("qhb.qbao.com", timeout=30)
        httpClient.request("POST", "/ajax/refreshBuilding.html", params, headers)
        response = httpClient.getresponse()
        responseStr = response.read().decode('utf-8')
        strResponse = json.loads(responseStr)
        nowCount = strResponse["data"]["onlineUser"]["raffleCount"]+strResponse["data"]["onlineUser"]["groupRaffleCount"]
        if(firstCount==0):
            firstCount =nowCount
        if(lastCount ==0):
            lastCount =nowCount
        totalCount = firstCount - nowCount
        preCount = lastCount -nowCount
        lastCount = nowCount
        print('\n'+string1+str(nowCount)+string2+str(totalCount)+string3+str(preCount))
        _thread.exit_thread() 

array = ["3956218", "819093", "130877", "727751", "177718"]
#array = ["130877", "177718", "819093"]
#array = ["130877"]
lastCount = 0
firstCount = 0
while lopper:
        try:
                for i in range(len(array)):
                        _thread.start_new_thread(monitor,(array[i],))
                _thread.start_new_thread(qhbCount,(1,))
                sleep(1)
        except Exception as ex:
                print(Exception,":",ex)




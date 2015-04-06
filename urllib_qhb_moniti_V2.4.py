# coding=utf-8

import urllib2
import urllib
import json
import time
import traceback
from time import sleep
import sys
import thread 
import threading

mylock = threading.RLock()  
ISOTIMEFORMAT='%Y-%m-%d %X'
lopper = True
headers = {"X-Forwarded-For":"10.0.0.1"}
string1 = "总数：".decode("utf-8").encode("utf-8")
string2 = "总投入：".decode("utf-8").encode("utf-8")
string3 = "单次投入：".decode("utf-8").encode("utf-8")
string4 = "兑奖中".decode("utf-8").encode("utf-8")
string5 = "大团".decode("utf-8").encode("utf-8")
string6 = "小团".decode("utf-8").encode("utf-8")

def monitor(owenId,index,sEcho):
	url = 'http://qhb.qbao.com/ajax/listGroup.html'
	values = {'sEcho':sEcho,
	'iColumns':7,
	'sColumns':',,,,,,',
	'iDisplayStart':index,
	'iDisplayLength':10,
	'mDataProp_0':0,
	'sSearch_1':'',
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
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	req.add_header('accept-encoding','gzip, deflate')
	req.add_header('referer','http://qhb.qbao.com/groupDetail/627107.html')
	req.add_header('accept','application/json, text/javascript, */*; q=0.01')
	req.add_header('content-type','application/x-www-form-urlencoded; charset=utf-8')
	req.add_header('accept-language','zh-cn,zh;q=0.8,en;q=0.6')
	req.add_header('X-Forwarded-For','10.0.0.1')
	req.add_header('user-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36')
	response = urllib2.urlopen(req)	
	the_page =response.read()
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
	#print owenId+" "+aaData[0]["status"]RAFFING
	countSmall = 0
	countLarge = 0
	for i in range(len(aaData)):
		if (aaData[i]["status"]=="RAFFING"):
			countPre = aaData[i]["raffleCount"]
			if countPre<250:
				countSmall=countSmall+1
			else:
				countLarge = countLarge+1
	if(countLarge+countSmall>1):
		if(countLarge>countSmall):
			print owenId+string5+str(countLarge)+"\r"
		else:
			print owenId+string6+str(countSmall)+"\r"
#num = str(aaData).count("RAFFING")
#	if num>=1:
#	    lopper = False
#	    print "\r\n"+time.strftime( ISOTIMEFORMAT, time.localtime() )
#	    print owenId+string4+str(num)
	thread.exit_thread()

def qhbCount(num):
	global lastCount
	global firstCount
        request=urllib2.Request("http://qhb.qbao.com/ajax/refreshBuilding.html",headers = headers)
        response = urllib2.urlopen(request)
        strResponse = json.loads(response.read())
        nowCount = strResponse["data"]["onlineUser"]["raffleCount"]+strResponse["data"]["onlineUser"]["groupRaffleCount"]
        if(firstCount==0):
            firstCount =nowCount
        if(lastCount ==0):
            lastCount =nowCount
	mylock.acquire()
        totalCount = firstCount - nowCount
        preCount = lastCount -nowCount
        lastCount = nowCount
        print string1+str(nowCount)+string2+str(totalCount)+string3+str(preCount)
	mylock.release()  
	thread.exit_thread() 

#850793#3956218#818109
array = ["850793","177718","130877","3392236","1419392","5462407"]
lastCount = 0
firstCount = 0
while lopper:
	try:
	    for i in range(len(array)):
		thread.start_new_thread(monitor,(array[i],0,1))
		#thread.start_new_thread(monitor,(array[i],10,2))
	    thread.start_new_thread(qhbCount,(1,))
	    sleep(0.5)
	except Exception,ex:
	    print Exception,":",ex

# -*- coding: utf-8 -*-
import requests
import re
import time
import qqmail
import ConfigParser
from bs4 import BeautifulSoup

url = "http://mis.teach.ustc.edu.cn/login.do"
session = requests.Session()
headers = {
    "Host":"mis.teach.ustc.edu.cn",
    #"Cookie":"JSESSIONID=0A41DCA3E6C96CB470CB912F4EB699DC",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36"
}

cf = ConfigParser.RawConfigParser()
cf.read("ustc.conf")
Username = cf.get("PersonalInfo", "Username")
Password = cf.get("PersonalInfo", "Password")
Xuenian = cf.get("PersonalInfo", "Xuenian")
_user = cf.get("PersonalInfo", "mail_user")
_pwd = cf.get("PersonalInfo", "mail_pwd")
_to = cf.get("PersonalInfo", "mail_to")
interval = int(cf.get("PersonalInfo", "interval"))
print "read conf done!"

formdata = {
    "sfyyzm":"0",
    "userbz":"s",
    "userCode":Username,
    "passWord":Password
}
chaxundata = {
    "xuenian":Xuenian,
    "chaxun":"",
    "px":"1",
    "zd":"0"
}

CurrList = []
def GetXuenianInfo():
    XuenianInfo = {}
    chengji = []
    XuenianInfo['xuefen'] = ''
    XuenianInfo['gpa'] = ''
    XuenianInfo['ave'] = ''
    info = session.post("http://mis.teach.ustc.edu.cn/querycjxx.do", data=chaxundata, headers=headers).text
    soup = BeautifulSoup(info,"html.parser")
    try:
        info1 = soup.body.table.tr.find_all("td", align="left")
        info2 = soup.body.find_all("table")[2].find_all("tr")
    except:
        info1 = soup.body.find_all("table")[1].tr.find_all("td", align="left")
        info2 = soup.body.find_all("table")[2].find_all("tr")
    if len(info2)-1 == len(CurrList):
        return None

    if len(info1)>1:
        XuenianInfo['xuefen'] = info1[0].text
        XuenianInfo['gpa'] = info1[4].text
        XuenianInfo['ave'] = info1[5].text

    for each in info2:
        sub = {}
        info3 = each.find_all("td")
        if len(info3) > 1:
            sub['kecheng'] = info3[2].text
            sub['fenshu'] = info3[4].text
            sub['xuefen'] = info3[6].text
            if sub not in CurrList:
                CurrList.append(sub)
                return sub
            #chengji.append(sub)
    #XuenianInfo['chengji'] = chengji
    #return XuenianInfo

def CheckUpdate():
    check = GetXuenianInfo()
    if check != None:
        qqmail.mail("",check["kecheng"]+" "+check["fenshu"],_user,_pwd,_to)


session.post(url,data = formdata,headers = headers)
count = 0
print "start working"
while(1):
    try:
        count = 0
        CheckUpdate()
    except:
        print "error"
        time.sleep(60)
        count = count + 1
        if(count == 10):
            qqmail.mail("","gg啦～",_user,_pwd,_to)
    time.sleep(interval)

# -*- coding: utf-8 -*-
import re
import pymysql
from os import path,system
import time
import json
import sys



#启动的时间
startTime = int(time.time())

#读取控制台输入
if len(sys.argv) != 2:
    print("运行格式:python test.py 日志文件名")
    sys.exit(-1)

logFile = sys.argv[1]

#读取配置文件
conf = open("conf.json").read()
conf = json.loads(conf,encoding='utf-8')

#数据库配置
db = conf['db']
#网站域名，这里指的是日志所属的域名
domain = conf['domain']

#读取文件大小
fileSize = path.getsize(logFile)

#过滤
r = re.compile(conf['dump']['fitter'],re.I)

#蜘蛛
#百度蜘蛛
bdSpider = re.compile('Baiduspider|baiduspider',re.I)
#搜狗蜘蛛
souguoSpider = re.compile('Sogou web spider|Sogou inst spider|Sogou spider2|Sogou blog|Sogou News Spider|Sogou Orion spider',re.I)
#360蜘蛛
haosouSpider = re.compile('360Spider|haosouspider',re.I)
#谷歌蜘蛛
googleSpider = re.compile('googlebot|googlebot-mobile|googlebot-image|mediapartners-google|adsbot-google',re.I)

log = open(logFile,'r',encoding='UTF-8')
connection = pymysql.connect(host=db['host'], user=db['user'], password=db['pwd'],db=db['database'],charset=db['charset'])
sql = "INSERT INTO `log` (`ip`,`path`,`ua`,`referer`,`datetime`,`status`,`spider`) VALUES (%s,%s,%s,%s,%s,%s,%s)"

#当前读取的文件大小
curSize = 0;

with connection.cursor() as cursor:
    for line in log:
        #计算当前已读取的进度
        curSize += len(line.encode(encoding='utf-8'))
        por = float(curSize/fileSize) * 100
        #计算当前已运行的时间
        runTime = int(time.time()) - startTime

        #清空并输出
        system('cls')
        print("当前进度:",por,"%")
        print("当前已运行:",runTime,"秒")

        if len(line) < 5 :
            continue

        tmp = line.split(" ")
        if r.search(tmp[6]) is not None:
            continue

        #ua
        ua = tmp[11:]
        ua = "".join(ua)
        ua = ua.replace("\n","")

        #time
        t = tmp[3]
        t = t[1:]
        timeArray = time.strptime(t, "%d/%b/%Y:%H:%M:%S")
        timeStamp = int(time.mktime(timeArray))

        #判断蜘蛛
        spider = 0
        if bdSpider.search(ua) is not None:
            spider = 1
        elif souguoSpider.search(ua) is not None:
            spider = 2
        elif haosouSpider.search(ua) is not None:
            spider = 3
        elif googleSpider.search(ua) is not None:
            spider = 4


        o = {
            "ip":tmp[0],
            "path":domain + tmp[6],
            "status":tmp[8],
            "referer":tmp[10],
            "ua":ua,
            "datetime":str(timeStamp),
            "spider":str(spider)
        }
        cursor.execute(sql, (o['ip'],o['path'],o['ua'],o['referer'],o['datetime'],o['status'],o['spider']))


connection.commit()
connection.close()
log.close()
# -*- coding: utf-8 -*-
import re
import pymysql
from os import path,system
import time
import json
import sys
import threading
import queue



lineQueue = queue.Queue()
dataQueue = queue.Queue()
wordQueue = queue.Queue()
progressDist = {"curSize":0,"readLine":0,"formatNum":0,"curData":0,"successData":0}


def readThreading(lq,wq,file):
    """
    读取日志文件
    """
    global progressDist
    f = open(file,'r',encoding='utf-8')
    for line in f:
        progressDist['readLine'] += 1
        #计算当前已读取的进度
        curSize = len(line.encode(encoding='utf-8'))
        progressDist['curSize'] += curSize
        if curSize > 20:
            lq.put(line)
    
    f.close()
    wq.put('readThreading')

def analysisThreading(lq,dq,wq,fitter):
    """
    分析
    """
    global progressDist
    #过滤
    r = re.compile(fitter)
    #蜘蛛
    #百度蜘蛛
    bdSpider = re.compile('Baiduspider|baiduspider',re.I)
    #搜狗蜘蛛
    souguoSpider = re.compile('Sogou web spider|Sogou inst spider|Sogou spider2|Sogou blog|Sogou News Spider|Sogou Orion spider',re.I)
    #360蜘蛛
    haosouSpider = re.compile('360Spider|haosouspider',re.I)
    #谷歌蜘蛛
    googleSpider = re.compile('googlebot|googlebot-mobile|googlebot-image|mediapartners-google|adsbot-google',re.I)

    while True:
        if wq.qsize() == 1 and lq.empty():
            wq.put('analysisThreading')
            break

        if lq.empty():
            time.sleep(0.1)
        else:
            line = lq.get()
            progressDist['formatNum'] += 1
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
            dq.put(o)
            progressDist['curData'] += 1


def addThreading(dq,wq,db):
    """数据入库"""
    global progressDist
    connection = pymysql.connect(host=db['host'], user=db['user'], password=db['pwd'],db=db['database'],charset=db['charset'])
    sql = "INSERT INTO `log` (`ip`,`path`,`ua`,`referer`,`datetime`,`status`,`spider`) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    with connection.cursor() as cursor:
        while True:
            if wq.qsize() == 2 and dq.empty():
                wq.put('addThreading')
                break;
            
            if dq.empty():
                time.sleep(1)
            else:
                o = dq.get()
                cursor.execute(sql, (o['ip'],o['path'],o['ua'],o['referer'],o['datetime'],o['status'],o['spider']))
                progressDist['successData'] += 1

    connection.commit()
    connection.close()

def progressThreading(wq,maxSize,startTime):
    """进度"""
    por = 0.00
    curSize = 0
    while True:
        if wq.qsize() == 3:
            wq.put('progressThreading')
            break;

        #日志读取进度
        if progressDist['curSize'] == 0:
            por = 0.00
        else:
            por = float(int(progressDist['curSize'])/maxSize) * 100
        #分析进度
        if progressDist['formatNum'] == 0 or progressDist['readLine'] == 0:
            fpor = 0.00
        else:
            fpor = float(int(progressDist['formatNum'])/int(progressDist['readLine'])) * 100
        #入库进度
        if progressDist['curData'] == 0 or progressDist['successData'] == 0:
            apor = 0.00
        else:
            apor = float(int(progressDist['successData'])/int(progressDist['curData'])) * 100
        #计算当前已运行的时间
        runTime = int(time.time()) - startTime

        #清空并输出
        system('cls')
        print("当前日志读取进度:",por,"%")
        print("当前读取",progressDist['readLine'],"行")
        print("当前分析进度:",fpor,"%")
        print("当前入库进度:",apor,"%")
        print("当前已运行:",runTime,"秒")
        time.sleep(1)



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


#启动任务
runFile = threading.Thread(target=readThreading,args=(lineQueue,wordQueue,logFile))
formatLine = threading.Thread(target=analysisThreading,args=(lineQueue,dataQueue,wordQueue,conf['dump']['fitter']))
addData = threading.Thread(target=addThreading,args=(dataQueue,wordQueue,db))
progress = threading.Thread(target=progressThreading,args=(wordQueue,fileSize,startTime))

runFile.start()
formatLine.start()
addData.start()
progress.start()

runFile.join()
formatLine.join()
addData.join()
progress.join()

print('数据导入完毕...')
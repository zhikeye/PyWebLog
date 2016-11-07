# -*- coding: utf-8 -*-

from flask import Flask,render_template,jsonify,request
import pymysql
import time
from app import dataUtil

#数据库信息
db = {}
#服务信息
server = {}
#网站
domain = ""

def getDb():
    connection = pymysql.connect(host=db['host'], user=db['user'], password=db['pwd'],db=db['database'],charset=db['charset'])
    return connection

#Flask
app = Flask(__name__)

#首页
@app.route('/',methods=['GET'])
def index():
    """首页"""
    conn = getDb()
    logNum = 0
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as `num` FROM `log`")
        d = cursor.fetchone()
        if d is not None:
            logNum = int(d[0])

    conn.close()
    return render_template('index.html',authorCont="不要问我默认端口为什么是9387~~",host=server['ip'],port=server['port'],domain=domain,navindex=1,logNum=logNum)


#24小时ip、pv统计图
@app.route('/datainfo',methods=['GET'])
def dataInfo():
    """每日详情数据"""
    return render_template('datainfo.html',navdatainfo=1)

@app.route('/api/datainfo',methods=['POST'])
def apiDataInfo():
    """每日详情数据api"""
    sData = request.form['logData']
    #时间字符串转换成时间戳
    timeArray = time.strptime(sData, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    conn = getDb()
    d = dataUtil.getDataInfo(timeStamp,conn)
    return jsonify(ip=d[0],pv=d[1])


#一天服务器响应状态图
@app.route('/webStatus',methods=['GET'])
def webStatus():
    """状态统计"""
    return render_template('webStatus.html',navwebStatus=1)

@app.route('/api/webStatus',methods=['POST'])
def apiWebStatus():
    """状态统计api"""
    sData = request.form['logData']
    #时间字符串转换成时间戳
    timeArray = time.strptime(sData, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    conn = getDb()
    d = dataUtil.getWebStatus(timeStamp,conn)
    return jsonify(data=d)


#指定日期蜘蛛24小时访问图
@app.route('/bot',methods=['GET'])
def bot():
    """状态统计"""
    return render_template('bot.html',navbot=1)

@app.route('/api/bot',methods=['POST'])
def apiBot():
    """状态统计api"""
    sData = request.form['logData']
    #时间字符串转换成时间戳
    timeArray = time.strptime(sData, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    #蜘蛛
    ua = request.form['bot']
    conn = getDb()
    d = dataUtil.getBot(timeStamp,conn,bot=ua)
    return jsonify(data=d)

#指定Url上下游
@app.route('/relation',methods=['GET'])
def relation():
    """状态统计"""
    return render_template('relation.html',navrelation=1)

@app.route('/api/relation',methods=['POST'])
def apiRelation():
    """状态统计api"""
    #起始时间
    sData = request.form['inpstart']
    timeArray = time.strptime(sData, "%Y-%m-%d")
    inpstart = int(time.mktime(timeArray))

    #结束时间
    sData = request.form['inpend']
    timeArray = time.strptime(sData, "%Y-%m-%d")
    inpend = int(time.mktime(timeArray)) + 86400
    #PATH
    path = request.form['url']
    conn = getDb()
    d = dataUtil.getRelation(timeStart=inpstart,timeEnd=inpend,conn=conn,path=path)
    return jsonify(data=d)

#指定时间内的服务器响应码的链接
@app.route('/status',methods=['GET'])
def statusPath():
    """状态统计"""
    return render_template('statusError.html',navstatus=1)

@app.route('/api/status',methods=['POST'])
def apiStatusPath():
    """状态统计api"""
    #起始时间
    sData = request.form['inpstart']
    timeArray = time.strptime(sData, "%Y-%m-%d")
    inpstart = int(time.mktime(timeArray))

    #结束时间
    sData = request.form['inpend']
    timeArray = time.strptime(sData, "%Y-%m-%d")
    inpend = int(time.mktime(timeArray)) + 86400

    #服务器返回码
    code = request.form['code']

    #条数
    limit = request.form['limit']
    conn = getDb()
    d = dataUtil.getStatusData(timeStart=inpstart,timeEnd=inpend,conn=conn,code=code,limit=limit)
    return jsonify(data=d)


def run(host='127.0.0.1',port=9387,debug=True):
    """运行"""
    app.run(host=host,port=port,debug=debug)
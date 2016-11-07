# -*- coding: utf-8 -*-

def getDataInfo(timeStamp,conn):
    """获取指定日期的ip和pv
    """
    ipData = []
    pvData = []
    pvSql = "SELECT COUNT(*) AS `num` FROM `log` WHERE `datetime` >= %s AND `datetime` < %s LIMIT 1"
    ipSql = "SELECT count(t.num) FROM (SELECT COUNT(*) AS `num` FROM `log` WHERE `datetime` >= %s AND `datetime` < %s GROUP BY `ip`) as t"
    with conn.cursor() as cursor:
        for i in range(0,24):
            start = timeStamp + i * 3600
            end = start + 3600
            #pv
            cursor.execute(pvSql,(str(start),str(end)))
            tPv = cursor.fetchone()
            if tPv is None:
                pvData.append(0)
            else:
                pvData.append(int(tPv[0]))

            #ip
            cursor.execute(ipSql,(str(start),str(end)))
            tIp = cursor.fetchone()
            if tIp is None:
                ipData.append(0)
            else:
                ipData.append(int(tIp[0]))


    conn.close()
    return (ipData,pvData)


def getWebStatus(timeStamp,conn):
    """获取指定日期的服务器响应占比
    """
    sql = "SELECT `status`,count(*) as num FROM `log` WHERE `datetime` >= %s AND `datetime` < %s GROUP BY `status`"
    j = []
    with conn.cursor() as cursor:
        start = timeStamp
        end = start + 86400
        cursor.execute(sql,(str(start),str(end)))
        d = cursor.fetchall()
        if d is not None:
            for i in d:
                j.append({"code":i[0],"num":i[1]})

    conn.close()
    return j

def getBot(timeStamp,conn,bot=1):
    """获取指定日期的蜘蛛曲线数据
    """
    sql = "SELECT count(*) as num FROM `log` WHERE `spider` = %s AND `datetime` >= %s AND `datetime` < %s"
    j = []
    with conn.cursor() as cursor:
        for i in range(0,24):
            start = timeStamp + i * 3600
            end = start + 3600
            #pv
            cursor.execute(sql,(str(bot),str(start),str(end)))
            d = cursor.fetchone()
            if d is None:
                j.append(0)
            else:
                j.append(int(d[0]))

    conn.close()
    return j


def getRelation(timeStart=0,timeEnd=0,conn={},path=""):
    """获取指定时间段指定地址的上下游
    """
    usql = "SELECT `referer`,count(*) as `num` FROM `log` WHERE  `path` = %s AND `datetime` >= %s AND `datetime` <= %s AND `referer` <> '-'  GROUP BY `referer` ORDER BY num DESC limit 20"
    nsql = "SELECT `path`,count(*) as `num` FROM `log` WHERE `referer` = %s AND `datetime` >= %s AND `datetime` <= %s  GROUP BY `path` ORDER BY num DESC limit 20"
    j = {}
    with conn.cursor() as cursor:
        #上游
        cursor.execute(usql,(path,str(timeStart),str(timeEnd)))
        d = cursor.fetchall()
        if d is None:
            j['pre'] = []
        else:
            j['pre'] = [i[0] for i in d]
        
        #下游
        cursor.execute(nsql,(path,str(timeStart),str(timeEnd)))
        d = cursor.fetchall()
        if d is None:
            j['next'] = []
        else:
            j['next'] = [i[0] for i in d]
        

    conn.close()
    return j

def getStatusData(timeStart=0,timeEnd=0,conn={},code="",limit=1000):
    """获取指定时间段指定的状态码
    """
    sql = "SELECT `path`,`status`,`datetime`,`referer` FROM `log` WHERE `status` = %s AND `datetime` >= %s AND `datetime` <= %s ORDER BY id DESC LIMIT "+limit
    j = {}
    f = ('path','status','datetime','referer')
    with conn.cursor() as cursor:
        cursor.execute(sql,(code,str(timeStart),str(timeEnd)))
        d = cursor.fetchall()
        if d is None:
            j = []
        else:
            j = [dict(zip(f,i)) for i in d]
        
        

    conn.close()
    return j
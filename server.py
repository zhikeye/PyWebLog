# -*- coding: utf-8 -*-

import app
import json

#读取配置文件
conf = open("conf.json").read()
conf = json.loads(conf,encoding='utf-8')

#数据库配置
db = conf['db']
app.db = db

app.server = conf['server']

app.domain = conf['domain']






if __name__ == '__main__':
    if app.server['debug'] == 1:
        debug = True
    else:
        debug = False 
    app.run(host=app.server['ip'],port=app.server['port'],debug=debug)
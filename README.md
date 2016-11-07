# PyWebLog 网站日志分析小工具

## 环境
1. Python3.5
2. Mysql

## 预览

![image](https://github.com/zhikeye/PyWebLog/blob/master/previewImages/1.png)
![image](https://github.com/zhikeye/PyWebLog/blob/master/previewImages/2.png)
![image](https://github.com/zhikeye/PyWebLog/blob/master/previewImages/3.png)


## 安装
```
pip install pymysql
pip install flask
```

## 导入日志
```
python Log.py 日志文件名
```

### 导入日志的格式

一般默认的都是这样的
```
111.206.36.15 - - [05/Nov/2016:03:35:04 +0800] GET / HTTP/1.1 200 6861 http://www.baidu.com/s?wd=www Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0 -
```

## 启动Web服务
```
python server.py
```
在浏览器访问*127.0.0.1:9387*即可

## conf.json配置文件
```
{
    #Mysql信息
    "db":{
        "host":"loaclhost",
        "database":"weblog",
        "port":"3306",
        "user":"root",
        "pwd":"root",
        "charset":"utf8"
    },
    "domain":"日志网站的域名",
    #web界面相关
    "server":{
        "port":9387,
        "ip":"127.0.0.1",
        "debug":1
    },
    #这里是日志访问路径过滤的正则，匹配的都不入库
    "dump":{
        "fitter":".js|.css|index.php|.jpg|.png|.gif|.ico"
    }
}
```

## 说明
这个小工具只是自己用下的，还有很多地方没弄好，性能也没优化的。

特别是导入日志文件的时候，如果文件非常大，需要的时间会很久；我自己是把日志文件分割后再分别导入，这样快很多。

如果有什么要的建议，可以告诉我~~

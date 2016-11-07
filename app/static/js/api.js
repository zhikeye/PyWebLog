var Api = function(){};
Api.prototype = {
    dataInfo:function(d,callback){
        $.post('/api/datainfo',d,function(j){
            callback(j);
        },"json");
    },
    webStatus:function(d,callback){
        $.post('/api/webStatus',d,function(j){
            callback(j);
        },"json");
    },
    bot:function(d,callback){
        $.post('/api/bot',d,function(j){
            callback(j);
        },"json");
    },
    relation:function(d,callback){
        $.post('/api/relation',d,function(j){
            callback(j);
        },"json");
    },
    serverStatus:function(d,callback){
        $.post('/api/status',d,function(j){
            callback(j);
        },"json");
    }
};


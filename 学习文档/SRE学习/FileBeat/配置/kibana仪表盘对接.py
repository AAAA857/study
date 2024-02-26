'''

    1. 默认filebeat自带了很多对应模块使用的kibanna仪表盘
    2， filebeat通过调用 kibana api 接口去上传


'''

'''
# 常用参数-kibana连接配置
 setup.kibana.url       //kibana 地址
 setup.kibana.protocol  //kibana协议 "http、https"
 setup.kibana.username  //kibana用户名
 setup.kibana.password  //kibana密码
 setup.kibana.path      //使用反向代理时 代理的请求路径
 setup.kibana.id        //kibana仪表盘空间
 setup.kibana.headers   //kibana请求设置的首部信息
 setup.kibana.ssl.enabled   //使用https时指定证书、私钥文件


# 仪表盘配置信息
setup.dashboards.enabled        //true表示加载仪表盘文件
setup.dashboards.directory      //仪表盘加载目录
setup.dashboards.url            //下载仪表盘地址
setup.dashboards.file           //加载仪表盘的zip文件
  
'''
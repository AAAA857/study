'''
    try_files： 用于检查uri是否存在，如果不存在或根据配置逐级检测

    使用场景:
        1. 404页面
        2. 页面跳转

    配置格式:
        指令配置格式:	try_files file ... uri;
                    try_files file ... =code;
        默认:	    —
        配置区域:	server, location
'''
'''使用样例'''

''' 检测路径实现跳转
    location /images/ {
        # $uri 检测输入路径是否存在，不存在将跳转此路径/images/default.gif
        try_files $uri /images/default.gif;
    }
    
    location = /images/default.gif {
        expires 30s;
    }
    
    location / {
    # 检测不存在将返回状态404
    try_files $uri $uri/index.html $uri.html =404;
    }


'''
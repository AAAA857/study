'''
    https://www.elastic.co/guide/en/logstash/7.12/plugins-inputs-http.html
    1. logstash 将会在宿主机监听一个端口
    2. 接受用户发送的PUT/POST请求，根据 Content-Type
    3. 使用此输入，您可以通过 http(s) 接收单行或多行事件
    4. 用户可以传递纯文本、JSON 或任何格式化数据，并对此输入使用相应的编解码器
    5. 可以设置 SSL 并通过 https 安全地发送数据，并使用多个选项，例如验证客户端的证书
'''

'''
# 常用参数
    port        //logstash监听端口
    host        //监听主机IP
    
    user        // 开启认证模式
    password    // 开启认证模式后密码
    ssl         //开启ssl配置
    ssl_certificate //ssl 证书文件
    ssl_key         // ssl 密钥文件
    threads     // 线程数
    max_content_length  // 请求最大字节
    
    
    response_headers    // 自定义logstash响应首部信息
    



'''
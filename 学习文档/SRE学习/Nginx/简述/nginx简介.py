'''

    nginx 是一个开源的静态web（拥有商业版本）、代理、邮件、缓存服务器，由俄罗斯开发，采用epoll（异步非阻塞）模型工作，因此适合大并发场景
，nginx采用数据零拷贝模式，nginx插件化

    nginx 进程：
        master； 主进程复制管理配置文件加载、work进程的生命周期管理
        work： 工作进程负责接受处理请求数据，采用epoll I/O模型工作

    nginx 热加载机制:
        当使用reload热加载配置时，nginx master进程会启动新的工作进程，新请求的数据都将进入新进程中，老的work进程当请求都结束后将会退出

    nginx 常用命令:
        nginx -V 查看支持的模块
        nginx -t 检测配置文件
        nginx -s 发送信号 stop 、reload 、quit
        nginx -c 指定配置文件
        nginx -g 传入启动选项，docker场景使用较多

        
'''

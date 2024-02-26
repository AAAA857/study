'''
# nginx启动进程使用的用户和组 ，安全限制低权限运行
user nginx nginx;
# 性能优化，nginx进程数自动识别 根据cpu核心数
worker_processes  auto;
# 性能优化，nginx CPU亲和性绑定，每个进程占用独立CPU 这样可以避免频繁做调度
worker_cpu_affinity auto;

# 后台运行
daemon on;

# 启动错误日志 全局字段，level=info 级别
error_log  logs/error.log  info;

#pid        logs/nginx.pid;

# 驱动相关配置，影响连接相关
events {
   # 性能优化，每个nginx进程最大连接数，应调整系统文件句柄数
    worker_connections  65535;
   # 性能优化，惊群配置，默认off当收到请求后，每个process都会收到通知，on表示只有需要工作的process接收到请求
   accept_mutex on;
   # 性能优化，默认一个进程接收一个请求，如果开启此选项，进程可以一次性接收所有新连接
   #
}


http {
    # 引yy用其他nginx配置文件，多配合虚拟主机使用
    include virtual_server/*.conf;
    include       mime.types;
    default_type  application/octet-stream;
    # access 日志记录格式
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;
    # 性能优化，零拷贝数据
    sendfile        on;
    # 数据合并请求后统一回复，节省带宽，但是相应速度会变慢
    #tcp_nopush     on;
    # 延迟0.2毫秒发送请求数据，前提是开启了keealive长连接
    #tcp_nodelay   off;
    #keepalive_timeout  0;
    # 长连接配置，请求会在配置的时间内一直存在连接状态
    keepalive_timeout  65;
    # 性能优化，压缩相应速度，节省带宽，但是消耗CPU性能
    #gzip  on;

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}



'''
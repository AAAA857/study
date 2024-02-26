'''
    安装方式:
        1。 rpm 需要epel源
        2. 编译安装

    官网地址：https://nginx.org/en/download.html

'''

'''
# 编译安装Nginx
1. 安装依赖
yum install gcc gcc-devel pcre cmake zlib zlib-devel openssl openssl-devel
2. 编译安装
groupadd nginx
useradd -S /bin/bash -g nginx -r -M nginx

--prefix    //安装路径
--user      //运行用户
--group     //运行组
--with-stream   //tcp|udp 代理
--with-stream_ssl_module
./configure  --prefix=/data/package/nginx-server --user=nginx --group=nginx --with-http_ssl_module --with-http_v2_module  --with-stream --with-stream_ssl_module --with-pcre

make && make install
'''
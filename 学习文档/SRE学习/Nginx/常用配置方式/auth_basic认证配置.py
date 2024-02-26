'''
    nginx 提供基础的认证配置，当有的访问页面内容需要认证时使用auth_basic功能很有用


    配置方式
        # 开关
        Syntax:	auth_basic string | off;
        Default:
        auth_basic off;
        Context:	http, server, location, limit_except
        # 认证本地密码文件
        # 密码生产key:value 格式可以保存多个用户
        # 密码需要加密生成,可使用openssl passwd 或htpasswd 工具生成
        Syntax:	auth_basic_user_file file;
        Default:	—
        Context:	http, server, location, limit_except
'''

'''配置样例'''

'''
    1、使用openssl 生成密码文件
        openssl passwd 123456
    2、保存到本地文件
        echo "abc:U0hffusn/9eLI" > conf/passwd
    3、开启认证功能
        server {
            listen 80;
            server_name www.abc.com;
            root /data/package/nginx-server/html;
            
            location =/ {
                index index.html;
            }
            
            location /login {
                # 开启认证
                auth_basic "on";
                auth_basic_user_file passwd;
            }
        }
    4、重启nginx
       /data/package/nginx-server/sbin/nginx -s reload
'''
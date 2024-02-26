# Python课程

## Socket编程:

### 网络基础:

#### OSI7模型:

<img src="https://pic1.zhimg.com/80/v2-2d62ba265be486cb94ab531912aa3b9c_720w.webp" alt="img" style="zoom:100%;" />

```python
'''
    OSI7层模型：
        应用层：   对应开发的应用程序如何httpd、nginx、ftp
        表示层：   数据格式的加密解密，让应用层能理解数据
        会话层：   应用程序的会话连接
        传输层：   对应端口
        网络层：    IP地址转换，不通网络之间标识符
        数据链路层：  MAC层用于数据帧的寻址和传递
        物理层：    网卡、网线、交换机，真实的物理设备用于传输数据包

    OSI5层模型: 通常大家将7层模型说层4层模型
        应用层
        传输层
        网络层
        数据链路层
        物理层


    SYN：表示一个新请求
    ACK： 表示一个确定有效
    RST：  表示TCP连接过程中出现异常必须重拾
    FIN：   表示之后不会发送数据包了，希望断开连接
    三次握手：
        1. 三次握手数据TCP协议特性
            1.1 client 发送一个syn + seq 的请求                                 SYN_SEND状态
            1.2 server 返回一个ack + syn +seq 的请求到client                     SYN_RCVD状态
            1.2 client 发送一个ack 确认报文 值为第二次server发送的seq+1             此时双方都处于ESTABLISHED状态
            1.3 随后client发送数据将发送

    四次挥手：
       1. 四次挥手属于TCP协议特性
          1.1 如果发送数据的是client并且数据发送完成想要断开，client 会发送一个FIN + seq          处于FIN-WAIT-1状态
          1.2 server 接收到FIN标识后返回一个ACk + seq 表示server 同意关闭连接但不是立即关闭       处于CLOS-WAIT状态
          1.3 server 在所有数据接收完成后发送一个FIN 请求到client                            处于LAST-ACK状态
          1.4 client 接收到server FIN请求后                                               处于FIN-WAIT-2状态
          1.5 client 在次回复一个ACK到server确认关闭                                       处于TIME-WAIT状态 在系统设置的时间内 此状态会被回收 此时端口被释放
          1.6 server 接收到最后一个确认ack后关闭连接                                         处于closd状态

'''
```

#### TCP三次握手:

![三次握手](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwNjA1MTEwNDA1NjY2?x-oss-process=image/format,png)

```python
'''
1.TCP服务器进程先创建传输控制块TCB，时刻准备接受客户进程的连接请求，此时服务器就进入了LISTEN（监听）状态；

2.TCP客户进程也是先创建传输控制块TCB，然后向服务器发出连接请求报文，这是报文首部中的同部位SYN=1，同时选择一个初始序列号 seq=x ，此时，TCP客户端进程进入了 SYN-SENT（同步已发送状态）状态。TCP规定，SYN报文段（SYN=1的报文段）不能携带数据，但需要消耗掉一个序号。

3.TCP服务器收到请求报文后，如果同意连接，则发出确认报文。确认报文中应该 ACK=1，SYN=1，确认号是ack=x+1，同时也要为自己初始化一个序列号 seq=y，此时，TCP服务器进程进入了SYN-RCVD（同步收到）状态。这个报文也不能携带数据，但是同样要消耗一个序号。

4.TCP客户进程收到确认后，还要向服务器给出确认。确认报文的ACK=1，ack=y+1，自己的序列号seq=x+1，此时，TCP连接建立，客户端进入

5.ESTABLISHED（已建立连接）状态。TCP规定，ACK报文段可以携带数据，但是如果不携带数据则不消耗序号。
当服务器收到客户端的确认后也进入ESTABLISHED状态，此后双方就可以开始通信了。

'''
# 数据包标识符号
SYN：表示一个新请求
ACK：表示一个确定有效
RST：表示TCP连接过程中出现异常必须重拾
FIN：表示之后不会发送数据包了，希望断开连接
```

#### TCP四次挥手:

![四次挥手](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwNjA2MDg0ODUxMjcy?x-oss-process=image/format,png)

```python
'''
1.客户端进程发出连接释放报文，并且停止发送数据。释放数据报文首部，FIN=1，其序列号为seq=u（等于前面已经传送过来的数据的最后一个字节的序号加1），此时，客户端进入FIN-WAIT-1（终止等待1）状态。 TCP规定，FIN报文段即使不携带数据，也要消耗一个序号。

2.服务器收到连接释放报文，发出确认报文，ACK=1，ack=u+1，并且带上自己的序列号seq=v，此时，服务端就进入了CLOSE-WAIT（关闭等待）状态。TCP服务器通知高层的应用进程，客户端向服务器的方向就释放了，这时候处于半关闭状态，即客户端已经没有数据要发送了，但是服务器若发送数据，客户端依然要接受。这个状态还要持续一段时间，也就是整个CLOSE-WAIT状态持续的时间。
客户端收到服务器的确认请求后，此时，客户端就进入FIN-WAIT-2（终止等待2）状态，等待服务器发送连接释放报文（在这之前还需要接受服务器发送的最后的数据）。

3.服务器将最后的数据发送完毕后，就向客户端发送连接释放报文，FIN=1，ack=u+1，由于在半关闭状态，服务器很可能又发送了一些数据，假定此时的序列号为seq=w，此时，服务器就进入了LAST-ACK（最后确认）状态，等待客户端的确认。

4.客户端收到服务器的连接释放报文后，必须发出确认，ACK=1，ack=w+1，而自己的序列号是seq=u+1，此时，客户端就进入了TIME-WAIT（时间等待）状态。注意此时TCP连接还没有释放，必须经过2∗ *∗MSL（最长报文段寿命）的时间后，当客户端撤销相应的TCB后，才进入CLOSED状态。

5.服务器只要收到了客户端发出的确认，立即进入CLOSED状态。同样，撤销TCB后，就结束了这次的TCP连接。可以看到，服务器结束TCP连接的时间要比客户端早一些。

'''
```

### Socket:

#### Socket描述:

```python

'''
	socket是基于C/S架构的，也就是说进行socket网络编程，通常需要编写两个py文件，一个服务端，一个客户端。

	首先，导入Python中的socket模块： import socket
'''

```

#### **Socket流程图：**![image.png-58.5kB](https://img2020.cnblogs.com/blog/1762677/202010/1762677-20201007160746044-1258982359.png)

#### Socket定义方法:

```python
'''

	在Python中，import socket后，用socket.socket()方法来创建套接字，语法格式如下：

		sk = socket.socket([family[, type[, proto]]])
			
		参数说明：
            family: 套接字家族，可以使AF_UNIX或者AF_INET。
            type: 套接字类型，根据是面向连接的还是非连接分为SOCK_STREAM或SOCK_DGRAM，也就是TCP和UDP的区别。
            protocol: 一般不填默认为0。
		
		family类型：
            AF_INET:    通过IP:端口方式传输数据，支持TCP/UDP协议
            AF_SOCKET:  本地进程间通信使用socket套接字文件通信

		
'''

```

|      socket类型       |                           **描述**                           |
| :-------------------: | :----------------------------------------------------------: |
|    socket.AF_UNIX     |              只能够用于单一的Unix系统进程间通信              |
|    socket.AF_INET     |                             IPv4                             |
|    socket.AF_INET6    |                             IPv6                             |
|  socket.SOCK_STREAM   |                     流式socket , for TCP                     |
|    socket.SOCK_RAW    | 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次，SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。 |
| socket.SOCK_SEQPACKET |                     可靠的连续数据包服务                     |
|   创建TCP Socket：    |      s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      |
|   创建UDP Socket：    |      s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)       |

|   family家族   |               描述               |
| :------------: | :------------------------------: |
| socket.AF_INET |    网络通信基于以太网协议传输    |
|   AF_SOCKET    | 本地通信基于socket文件描述符通信 |

#### Socket服务端方法:

| 方法                  | 描述                                                         |
| --------------------- | ------------------------------------------------------------ |
| **s.bind()**          | 绑定地址（host,port）到套接字，在AF_INET下,以元组（host,port）的形式表示地址。 |
| **s.listen(backlog)** | 开始监听。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。 |
| **s.accept()**        | 被动接受客户端连接,(阻塞式)等待连接的到来，并返回（conn,address）二元元组,其中conn是一个通信对象，可以用来接收和发送数据。address是连接客户端的地址。 |

#### Socket客户端方法:

| 方法                   | 描述                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **s.connect(address)** | 客户端向服务端发起连接。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。 |
| s.connect_ex()         | connect()函数的扩展版本,出错时返回出错码,而不是抛出异常      |

#### Socket公共方法:

| 方法                                 | 描述                                                         |
| :----------------------------------- | ------------------------------------------------------------ |
| **s.recv(bufsize)**                  | 接收数据，数据以bytes类型返回，bufsize指定要接收的最大数据量。 |
| **s.send()**                         | 发送数据。返回值是要发送的字节数量。                         |
| **s.sendall()**                      | 完整发送数据。将数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。 |
| s.recvform()                         | 接收UDP数据，与recv()类似，但返回值是（data,address）。其中data是包含接收的数据，address是发送数据的套接字地址。 |
| s.sendto(data,address)               | 发送UDP数据，将数据data发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。 |
| **s.close()**                        | 关闭套接字，必须执行。                                       |
| s.getpeername()                      | 返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。  |
| s.getsockname()                      | 返回套接字自己的地址。通常是一个元组(ipaddr,port)            |
| s.setsockopt(level,optname,value)    | 设置给定套接字选项的值。                                     |
| s.getsockopt(level,optname[.buflen]) | 返回套接字选项的值。                                         |
| s.settimeout(timeout)                | 设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如connect()） |
| s.gettimeout()                       | 返回当前超时期的值，单位是秒，如果没有设置超时期，则返回None。 |
| s.fileno()                           | 返回套接字的文件描述符。                                     |
| s.setblocking(flag)                  | 如果flag为0，则将套接字设为非阻塞模式，否则将套接字设为阻塞模式（默认值）。非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。 |
| s.makefile()                         | 创建一个与该套接字相关连的文件                               |

#### Socket编程思路:

```python
'''
服务端：

	1.创建套接字，绑定套接字到本地IP与端口：socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.bind()
	2.开始监听连接：s.listen()
	3.进入循环，不断接受客户端的连接请求：s.accept()
	4.接收传来的数据，或者发送数据给对方：s.recv() , s.sendall()
	5.传输完毕后，关闭套接字：s.close()

客户端:

    1.创建套接字，连接服务器地址：socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.connect()
    2.连接后发送数据和接收数据：s.sendall(), s.recv()
    3.传输完毕后，关闭套接字：s.close()
    
'''
   Python的socket编程，通常可分为TCP和UDP编程两种，前者是带连接的可靠传输服务，每次通信都要握手，结束传输也要挥手，数据会被检验，是使用最广的通用模式；后者是不带连接的传输服务，简单粗暴，不加控制和检查的一股脑将数据发送出去的方式，但是传输速度快，通常用于安全和可靠等级不高的业务场景，比如文件下载。
```

### TCP模式编程:

```python
import socket


def Server_S(*args,**kwargs):
    print(kwargs)
    # 创建一个socket对象
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 为创建的socket对象绑定一个地址
    s.bind((kwargs.get('host'),kwargs.get('port')))

    # 定义socket连接池大小
    s.listen(kwargs.get('bucket_size'))

    # 开始listen
    # 此处循环用于循环accept连接
    while True:
        # accept 将会阻塞住，等待client连接
        # accept 返回俩个连接信息，conn表示client的连接socket对象，addr表示client ip:port信息
        print('开始等待连接')
        conn,addr = s.accept()
        print(addr)

        while True:

            data = conn.recv(1024)
            # print('收到来自[%s]的一条消息: %s'% (conn,data.decode('utf-8')))
			
            # 判断recv接收为空跳出recv循环，表示客户端已经不在发送数据
            if not  data: break
            print(data.decode('utf-8'))
            # server 返回消息
            # conn.send(data.upper())

if __name__ == '__main__':
    print(Server_S(host='127.0.0.1',port=8888,bucket_size=10))
    
        
# client
import socket
import time

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',8888))

while True:
    client.send('abc'.encode('utf-8'))
    time.sleep(5)
```

#### TCP粘包:

```shell
# 什么是粘包？
  发送方发送两个字符串”hello”+”world”，接收方却一次性接收到了”helloworld”。

# TCP/UDP那个协议会出现粘包？
  1.TCP协议会出现粘包，UDP协议不会出现粘包，
  2.有时候，TCP为了提高网络的利用率，会使用一个叫做Nagle的算法。该算法是指，发送端即使有要发送的数据，如果很少的话，会延迟发送。如果应用层给TCP传送数据很快的话，就会把两个应用层数据包“粘”在一起，TCP最后只发一个TCP数据包给接收端。
# UDP
   1.不会使用块的合并优化算法这样
   2.UDP支持的是一对多的模式，所以接收端的skbuff(套接字缓冲区）采用了链式结构来记录每一个到达的UDP包，在每个UDP包中就有了消息头（消息来源地址，端口等信息），这样，对于接收端来说，就容易进行区分处理了。

```

##### 代码案例:

```python
'''
	server:
        1. 下面案例是采用TCP协议编写
        2. 接收client发送的命令并运行
        3. 返回命令执行结果
	client:
		1. client 发送命令
		2. 接收数据
'''
# server
import socket
import subprocess

class Server(object):

    def __init__(self,ip,port,listen=10):
        self.ip = ip
        self.port = port
        self.s = self.Server_Object()
        self.listen = listen
    def Server_Object(self):
        '''TCP'''
        return socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def __enter__(self):
        print('执行enter')
        self.s = self.Server_Object()
        self.s.bind((self.ip,self.port))
        self.s.listen(self.listen)
        return self.s
    def __exit__(self, exc_type, exc_val, exc_tb):

        self.s.close()

    def action(self,*args,**kwargs):

        comm = args[0]
        print(comm)
        res = subprocess.Popen(args=comm, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        # print(res.stdout.readlines())
        data = res.stdout.read()
        return data

    def Send_Mes(self,c,mes):
        print(mes)
        c.send(mes)

if __name__ == '__main__':

    obj = Server(ip='127.0.0.1',port=8889)

    with obj as s:
        while True:
            print('TCP开始监听')
            client_socket,client_address = s.accept()

            print(client_address)

            while True:
                '''接收数据'''
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    res = obj.action(data.decode('utf-8'))

                    obj.Send_Mes(c=client_socket,mes=res)
                except Exception as E:
                    client_socket.close()
                    break
# client
import socket
import time
# -*- coding: utf-8 -*-

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',8889))
while True:
    action = input('命令:').strip()
    client.send(action.encode('utf-8'))
    '''
    	此处只会读取client端自己的内存缓存区1024字节，TCP流式字节读取那么下次将继续读取剩下的缓存区数据
    '''
    d = client.recv(1024)
    print(d.decode('gbk'))
```

### UDP模式编程:

```shell
UDP（用户数据报协议）是一个与 IP 协议 一起使用的长期协议，用于在传输速度和效率比安全性和可靠性更重要的场合下发送数据。

UDP 使用一个简单的、具有最小协议机制的无连接通信模型。UDP 使用校验和保证数据完整性，使用端口号以区分数据发送方和接收方中不同的应用程序。它无需握手会话，即将不可靠的底层网络直接暴露给了用户的应用程序：不保证消息交付、不保证交付顺序也不保证消息不重复。如果需要网络接口层面的纠错功能，则应用程序可以使用为此目的设计的传输控制协议（TCP）或者流控制传输协议（SCTP）。
```

#### 代码案例:

##### NTP服务:

```python

# server 
import socket
import time
class Server(object):

    def __init__(self,ip,port,listen=5):
        self.ip = ip
        self.port = port
        self.s = self.Socket_Server()
        self.listen = listen
    def Socket_Server(self):
        return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def Bind_Server(self):
        self.s.bind((self.ip,self.port))
        return self.s

    def __call__(self, *args, **kwargs):
        s = self.Bind_Server()
        print('开始监听')
        while True:
            data, addr = s.recvfrom(1024)
            if data.decode() == 'time':
                T = time.strftime('%Y-%m-%d %X')
                s.sendto(T.encode('utf-8'),addr)

if __name__ == '__main__':

    obj = Server('127.0.0.1',8888)
    obj()


# client
import socket
import sys,time

print(sys.getdefaultencoding())
udp_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    udp_client.sendto('time'.encode('utf-8'),('127.0.0.1',8888))
    d,a = udp_client.recvfrom(1024)
    print(d)
    time.sleep(10)

```



# Linux SRE课程:

## Nginx:

### 内置变量:

```shell

# 返回客户端真实客户端地址
  echo $remote_addr;
# 放回uri请求参数
  echo $args;
# 返回请求uri对应的root目录
  echo $document_root;
# 返回请求对应的主机名称
  echo $host;
# 返回客户端请求的浏览器信息
  echo $http_user_agent;
# 如果请求携带cooike将返回
  echo $http_cookie;
# 请求协议
  echo $scheme;
# 客户端请求发起的端口
  echo $remote_port;
# 客户端如果认证对应的用户明
  echo $remote_user;
# 请求uri加参数
  echo $request;
# 请求大小
  echo $request_length;
# 请求的协议
  echo $request_method;
# 客户端请求的uri与包含请求的参数
  echo $request_uri;
# 客户端请求的uri不包含参数
  echo $uri;

```

### 自定义变量:

```shell
Syntax:	set $variable value;
Default:	—
Context:	server


# 自定义变量：当内置变量不满足要求时可以自定定义需要的特定值变量属性

```

### 自定义访问日志:

```shell
  访问日志是记录客户端即用户的具体请求内容信息，而在全局配置模块中的error_log是记录nginx服务
器运行时的日志保存路径和记录日志的level，因此两者是不同的，而且Nginx的错误日志一般只有一
个，但是访问日志可以在不同server中定义多个，定义一个日志需要使用access_log指定日志的保存路
径，使用log_format指定日志的格式，格式中定义要保存的具体日志内容。
访问日志由 ngx_http_log_module 模块实现

Syntax: access_log path [format [buffer=size] [gzip[=level]] [flush=time] 
[if=condition]];
access_log off; #关闭访问日志
Default: 
access_log logs/access.log combined;
Context: http, server, location, if in location, limit_except



#注意:此指令只支持http块,不支持server块
log_format nginx_format1  '$remote_addr - $remote_user [$time_local] "$request" 
'	
					'$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"'
                      '$server_name:$server_port';

#注意:此指令一定要在放在log_format命令后
access_log logs/access.log nginx_format1;


#重启nginx并访问测试日志格式
==> /apps/nginx/logs/access.log <==
10.0.0.1 - - [22/Feb/2019:08:44:14 +0800] "GET /favicon.ico HTTP/1.1" 404 162 "-
" "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/2
0100101 Firefox/65.0" "-"www.magedu.org:80
```

### 自定义json格式日志

```shell
	nginx 的默认访问日志记录内容相对比较单一，默认的格式也不方便后期做日志统计分析，生产环境中
通常将nginx日志转换为json日志，然后配合使用ELK做日志收集,统计和分析。

log_format access_json '{"@timestamp":"$time_iso8601",'
        '"host":"$server_addr",'
        '"clientip":"$remote_addr",'
        '"size":$body_bytes_sent,'
        '"responsetime":$request_time,' #总的处理时间
        '"upstreamtime":"$upstream_response_time",'
        '"upstreamhost":"$upstream_addr",'   #后端应用服务器处理时间
        '"http_host":"$host",'
        '"uri":"$uri",'
        '"xff":"$http_x_forwarded_for",'
         '"referer":"$http_referer",'
        '"tcp_xff":"$proxy_protocol_addr",'
        '"http_user_agent":"$http_user_agent",'
        '"status":"$status"}';
access_log /apps/nginx/logs/access_json.log access_json;
     
#重启Nginx并访问测试日志格式,参考链接:http://json.cn/
{"@timestamp":"2019-02-
22T08:55:32+08:00","host":"10.0.0.8","clientip":"10.0.0.1","size":162,"responset
ime":0.000,"upstreamtime":"-","upstreamhost":"-
","http_host":"www.magedu.org","uri":"/favicon.ico","xff":"-","referer":"-
","tcp_xff":"","http_user_agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; 
rv:65.0) Gecko/20100101 Firefox/65.0","status":"404"}

```

### Nginx压缩功能:

```shell
#  Nginx支持对指定类型的文件进行压缩然后再传输给客户端，而且压缩还可以设置压缩比例，压缩后的文件大小将比源文件显著变小，这样有助于降低出口带宽的利用率，降低企业的IT支出，不过会占用相应的CPU资源。

#Nginx对文件的压缩功能是依赖于模块 ngx_http_gzip_module,默认是内置模块

#官方文档： https://nginx.org/en/docs/http/ngx_http_gzip_module.html

# 配置指令如下：
#启用或禁用gzip压缩，默认关闭
gzip on | off; 
#压缩比由低到高从1到9，默认为1,级别越高压缩比例越大同样cpu使用率较大增加
gzip_comp_level level;
#禁用IE6 gzip功能
gzip_disable "MSIE [1-6]\."; 
#gzip压缩的最小文件，小于设置值的文件将不会压缩
gzip_min_length 1k; 
#启用压缩功能时，协议的最小版本，默认HTTP/1.1
gzip_http_version 1.0 | 1.1; 
#指定Nginx服务需要向服务器申请的缓存空间的个数和大小,平台不同,默认:32 4k或者16 8k;
gzip_buffers number size;  
#指明仅对哪些类型的资源执行压缩操作;默认为gzip_types text/html，不用显示指定，否则出错
gzip_types mime-type ...; 
#如果启用压缩，是否在响应报文首部插入“Vary: Accept-Encoding”,一般建议打开
gzip_vary on | off; 
#预压缩，即直接从磁盘找到对应文件的gz后缀的式的压缩文件返回给用户，无需消耗服务器CPU
#注意: 来自于ngx_http_gzip_static_module模块
gzip_static on | off;
#重启nginx并进行访问测试压缩功能
[root@centos8 ~]# cp /apps/nginx/logs/access.log /data/nginx/html/pc/m.txt




```

未开启压缩功能：![img](file:///C:\Users\THINKPAD\AppData\Local\Temp\\BaiduHi\5AB27134-1914-4AA1-8435-D56C458B27F6.jpg)

开启压缩功能:![image-20240103130502133](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240103130502133.png)

### Nginx全栈SSL:

#### SSL流程:

![image-20240103131723771](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240103131723771.png)

```shell
https 实现过程如下：
	1.客户端发起HTTPS请求：
	  客户端访问某个web端的https地址，一般都是443端口
	2.服务端的配置：
	  采用https协议的服务器必须要有一套证书，可以通过一些组织申请，也可以自己制作，目前国内很多网站都自己做的，当你访问一个网站的时候提示证书不可信任就表示证书是自己做的，证书就是一个公钥和私钥匙，就像一把锁和钥匙，正常情况下只有你的钥匙可以打开你的锁，你可以把这个送给别人让他锁住一个箱子，里面放满了钱或秘密，别人不知道里面放了什么而且别人也打不开，只有你的钥匙是可以打开的。
	3.传送证书：
	  服务端给客户端传递证书，其实就是公钥，里面包含了很多信息，例如证书得到颁发机构、过期时间等等。
	4.客户端解析证书：
	  这部分工作是有客户端完成的，首先回验证公钥的有效性，比如颁发机构、过期时间等等，如果发现异常则会弹出一个警告框提示证书可能存在问题，如果证书没有问题就生成一个随机值，然后用证书对该随机值进行加密，就像2步骤所说把随机值锁起来，不让别人看到。
	5.传送4步骤的加密数据：
      就是将用证书加密后的随机值传递给服务器，目的就是为了让服务器得到这个随机值，以后客户端和服务端的通信就可以通过这个随机值进行加密解密了。
	6.服务端解密信息：
      服务端用私钥解密5步骤加密后的随机值之后，得到了客户端传过来的随机值(私钥)，然后把内容通过该值进行对称加密，对称加密就是将信息和私钥通过算法混合在一起，这样除非你知道私钥，不然是无法获取其内部的内容，而正好客户端和服务端都知道这个私钥，所以只要机密算法够复杂就可以保证数据的安全性。
	7.传输加密后的信息:
	  服务端将用私钥加密后的数据传递给客户端，在客户端可以被还原出原数据内容。
	8.客户端解密信息：
	  客户端用之前生成的私钥获解密服务端传递过来的数据，由于数据一直是加密的，因此即使第三方获取到数据也无法知道其详细内容。
```

####  https配置参数：

```shell
	nginx 的https 功能基于模块ngx_http_ssl_module实现，因此如果是编译安装的nginx要使用参数
ngx_http_ssl_module开启ssl功能，但是作为nginx的核心功能，yum安装的nginx默认就是开启的，编
译安装的nginx需要指定编译参数--with-http_ssl_module开启
	
	官方文档： https://nginx.org/en/docs/http/ngx_http_ssl_module.html
	

配置参数如下：
#为指定的虚拟主机配置是否启用ssl功能，此功能在1.15.0废弃，使用listen [ssl]替代
ssl on | off;   
listen 443 ssl;

#指向包含当前虚拟主机和CA的两个证书信息的文件，一般是crt文件
ssl_certificate /path/to/file;
#当前虚拟主机使用的私钥文件，一般是key文件
ssl_certificate_key /path/to/file;
#支持ssl协议版本，早期为ssl现在是TLS，默认为后三个
ssl_protocols [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2]; 
#配置ssl缓存
ssl_session_cache off | none | [builtin[:size]] [shared:name:size];

   off： #关闭缓存
   none:  #通知客户端支持ssl session cache，但实际不支持
   builtin[:size]：#使用OpenSSL内建缓存，为每worker进程私有
   [shared:name:size]：#在各worker之间使用一个共享的缓存，需要定义一个缓存名称和缓存空间大
小，一兆可以存储4000个会话信息，多个虚拟主机可以使用相同的缓存名称


#客户端连接可以复用ssl session cache中缓存的有效时长，默认5m
ssl_session_timeout time;
```

#### 自签名证书:

```shell
#自签名CA证书
[root@centos8 ~]# cd /apps/nginx/
[root@centos8 nginx]# mkdir certs
[root@centos8 nginx]# cd certs/
[root@centos8 nginx]# openssl req -newkey rsa:4096 -nodes -sha256 -keyout 
ca.key -x509 -days 3650 -out ca.crt #自签名CA证书
Generating a 4096 bit RSA private key
.................++
.....
Country Name (2 letter code) [XX]:CN #国家代码
State or Province Name (full name) []:BeiJing   #省份
Locality Name (eg, city) [Default City]:Beijing #城市名称
Organization Name (eg, company) [Default Company Ltd]:magedu.Ltd #公司名称
Organizational Unit Name (eg, section) []:magedu #部门
Common Name (eg, your name or your server's hostname) []:ca.magedu.org #通用名称
Email Address []: #邮箱
[root@centos8 certs]# ll ca.crt 
-rw-r--r-- 1 root root 2118 Feb 22 12:10 ca.crt

#自制key和csr文件
[root@centos8 certs]# openssl req -newkey rsa:4096 -nodes -sha256 -keyout 
www.magedu.org.key     -out www.magedu.org.csr 
Generating a 4096 bit RSA private key
........................................................................++
......
Country Name (2 letter code) [XX]:CN
State or Province Name (full name) []:BeiJing
Locality Name (eg, city) [Default City]:BeiJing
Organization Name (eg, company) [Default Company Ltd]:magedu.org
Organizational Unit Name (eg, section) []:magedu.org
Common Name (eg, your name or your server's hostname) []:www.magedu.org
Email Address []:2973707860@qq.com
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:      
An optional company name []:
[root@centos8 certs]# ll
total 16
-rw-r--r-- 1 root root 2118 Feb 22 12:10 ca.crt
-rw-r--r-- 1 root root 3272 Feb 22 12:10 ca.key
-rw-r--r-- 1 root root 1760 Feb 22 12:18 www.magedu.org.csr
-rw-r--r-- 1 root root 3272 Feb 22 12:18 www.magedu.org.key

#签发证书
[root@centos8 certs]# openssl x509 -req -days 3650 -in www.magedu.org.csr -CA 
ca.crt -CAkey ca.key -CAcreateserial -out www.magedu.org.crt

#验证证书内容
[root@centos8 certs]# openssl x509 -in www.magedu.org.crt -noout -text 
Certificate:
   Data:
       Version: 1 (0x0)
       Serial Number:
           bb:76:ea:fe:f4:04:ac:06
   Signature Algorithm: sha256WithRSAEncryption
       Issuer: C=CN, ST=BeiJing, L=Beijing, O=magedu.Ltd, OU=magedu, 
CN=magedu.ca/emailAddress=2973707860@qq.com
       Validity
           Not Before: Feb 22 06:14:03 2019 GMT
           Not After : Feb 22 06:14:03 2020 GMT
       Subject: C=CN, ST=BeiJing, L=BeiJing, O=magedu.org, OU=magedu.org, 
CN=www.magedu.org/emailAddress=2973707860@qq.com
       Subject Public Key Info:
           Public Key Algorithm: rsaEncryption
               Public-Key: (4096 bit)
                
#合并CA和服务器证书成一个文件,注意服务器证书在前
[root@centos8 certs]#cat www.magedu.org.crt ca.crt > www.magedu.org.pem





# location 配置强转
location / {
	root /data/nginx/html/pc;
 	if ( $scheme = http ) {
    	rewrite ^/(.*)$ https://www.magedu.org/$1 redirect;         
    } 
}


```

#### Nginx开启https配置:

```shell
server {
        listen 8888 ssl;
        ssl_certificate /data/package/nginx-server/secret/cn1.a.64ip.top.crt;
        ssl_certificate_key /data/package/nginx-server/secret/cn1.a.64ip.top.key;

        server_name cn1.a.64ip.top;
        root  /var/www/html;

        location =/ {
      		  if ($scheme = "http") {
                       rewrite ^/(.*)$ https:/cn1.a.64ip.top:30001/$1 redirect; 
                }
                index index.html;
                #try_files $uri /default/index.html;
                #auth_basic "on";
                #auth_basic_user_file password;
        }
}
```

### Nginx Rewrite重写:

```shell
   Nginx服务器利用 ngx_http_rewrite_module 模块解析和处理rewrite请求，此功能依靠 PCRE(perlcompatible regular expression)，因此编译之前要安装PCRE库，rewrite是nginx服务器的重要功能之一，用于实现URL的重写，URL的重写是非常有用的功能，比如它可以在我们改变网站结构之后，不需要客户端修改原来的书签，也无需其他网站修改我们的链接，就可以设置为访问，另外还可以在一定程度上提高网站的安全性。
   
   官方文档: https://nginx.org/en/docs/http/ngx_http_rewrite_module.html
   
   break 、if、return、 rewrite和set指令按以下顺序处理 ：
   
   
```

#### if语句:

```shell
# 语法结构
if ($slow) {
    limit_rate 10k;
    break;
}


# if 匹配规则
= 					#比较变量和字符串是否相等，相等时if指令认为该条件为true，反之为false
!=  				#比较变量和字符串是否不相等，不相等时if指令认为条件为true，反之为false
~ 					#区分大小写字符，可以通过正则表达式匹配，满足匹配条件为真，不满足匹配条件为假
!~ 					#区分大小写字符,判断是否匹配，不满足匹配条件为真，满足匹配条件为假
~* 					#不区分大小写字符，可以通过正则表达式匹配，满足匹配条件为真，不满足匹配条件为假
!~*					#不区分大小字符,判断是否匹配，满足匹配条件为假，不满足匹配条件为真
-f 和 !-f 			#判断请求的文件是否存在和是否不存在
-d 和 !-d 			#判断请求的目录是否存在和是否不存在
-x 和 !-x 			#判断文件是否可执行和是否不可执行
-e 和 !-e 			#判断请求的文件或目录是否存在和是否不存在(包括文件，目录，软链接)


#示例：

location /main {
  index index.html;
  default_type text/html;
  if ( $scheme = http ){
   echo "if-----> $scheme";
  }
  if ( $scheme = https ){
   echo "if ----> $scheme";
 }
 
  #if (-f $request_filename) {
  #  echo "$request_filename is exist";
  #}
  if (!-e $request_filename) {
    echo "$request_filename is not exist";
    #return 409;
 }
}
```

#### set语句:

```shell
  指定key并给其定义一个变量，变量可以调用Nginx内置变量赋值给key，另外set定义格式为set $key
value，value可以是text, variables和两者的组合。

# 式例
location /main {
 root /data/nginx/html/pc;
 index index.html;
 default_type text/html;
  set $name magedu;
  echo $name;
  set $my_port $server_port;
  echo $my_port;
}

```

#### break语句:

```shell
  用于中断当前相同作用域(location)中的其他Nginx配置，与该指令处于同一作用域的Nginx配置中，位
于它前面的配置生效，位于后面的 ngx_http_rewrite_module 模块中指令就不再执行，Nginx服务器
在根据配置处理请求的过程中遇到该指令的时候，回到上一层作用域继续向下读取配置，该指令可以在
server块和locationif块中使用

#注意:
 如果break指令在location块中后续指令还会继续执行,只是不执行 ngx_http_rewrite_module 模块的指令,其它指令还会执行使用语法如下：

location /main {
	 root /data/nginx/html/pc;
 	index index.html;
 	default_type text/html;
  	set $name magedu;
  	echo $name;
 	break;  #location块中break后面指令还会执行
  	set $my_port $server_port;
  	echo $my_port;
}
```

#### return语句:

```shell
   return用于完成对请求的处理，并直接向客户端返回响应状态码，比如:可以指定重定向URL(对于特殊重
定向状态码，301/302等) 或者是指定提示文本内容(对于特殊状态码403/500等)，处于此指令后的所有
配置都将不被执行，return可以在server、if 和 location块进行配置中。

# 语法格式：
  return code; #返回给客户端指定的HTTP状态码
  return code [text]; #返回给客户端的状态码及响应报文的实体内容，可以调用变量,其中text如果有空格,需要用单或双引号
  return code URL; #返回给客户端的URL地址
  
# 示例：
  location / {
 	root /data/nginx/html/pc;
 	default_type text/html;
 	index index.html;
   	if ( $scheme = http ){
    #return 666;
    #return 666 "not allow http";
    #return 301 http://www.baidu.com;
   	return 500 "service error";
    echo "if-----> $scheme"; #return后面的将不再执行
  }


```

#### rewrite语句:

```shell
  通过正则表达式的匹配来改变URI，可以同时存在一个或多个指令，按照顺序依次对URI进行匹配，rewrite主要是针对用户请求的URL或者是URI做具体处理.
  官方文档：https://nginx.org/en/docs/http/ngx_http_rewrite_module.html#rewrite
  rewrite可以配置在 server、location、if
  
  
 # 语法格式 ：
 rewrite regex replacement [flag];
 
 
 rewrite将用户请求的URI基于regex所描述的模式进行检查，匹配到时将其替换为表达式指定的新的URI
# 注意：
 如果在同一级配置块中存在多个rewrite规则，那么会自下而下逐个检查;被某条件规则替换完成后，会重新一轮的替换检查，隐含有循环机制,但不超过10次;如果超过，提示500响应码，[flag]所表示的标志位用于控制此循环机制如果替换后的URL是以http://或https://开头，则替换结果会直接以重定向返回给客户端, 即永久重定向301.
```

##### 正则:

```shell
# 正则表达式格式
. 	#匹配除换行符以外的任意字符
\w 	#匹配字母或数字或下划线或汉字
\s 	#匹配任意的空白符
\d 	#匹配数字
\b 	#匹配单词的开始或结束
^ 	#匹配字付串的开始
$ 	#匹配字符串的结束
* 	#匹配重复零次或更多次
+ 	#匹配重复一次或更多次
? 	#匹配重复零次或一次
(n) #匹配重复n次
{n,} #匹配重复n次或更多次
{n,m} #匹配重复n到m次
*? #匹配重复任意次，但尽可能少重复
+? #匹配重复1次或更多次，但尽可能少重复
?? #匹配重复0次或1次，但尽可能少重复
{n,m}? #匹配重复n到m次，但尽可能少重复
{n,}? #匹配重复n次以上，但尽可能少重复
\W  #匹配任意不是字母，数字，下划线，汉字的字符
\S #匹配任意不是空白符的字符
\D #匹配任意非数字的字符
\B #匹配不是单词开头或结束的位置
[^x] #匹配除了x以外的任意字符
[^magedu] #匹配除了magedu 这几个字母以外的任意字符
```

##### flag使用介绍:

```shell
  利用nginx的rewrite的指令，可以实现url的重新跳转，rewrite有四种不同的flag，分别是:
  	redirect(临时重定向302)
  	permanent(永久重定向301)
  	break和last。	
  其中前两种是跳转型的flag，后两种是代理型
  
  	**跳转型指由客户端浏览器重新对新地址进行请求**
  	**代理型是在WEB服务器内部实现跳转**
  	
  	
redirect;
#临时重定向，重写完成后以临时重定向方式直接返回重写后生成的新URL给客户端，由客户端重新发起请求;
使用相对路径,或者http://或https://开头，状态码：302
permanent;
#重写完成后以永久重定向方式直接返回重写后生成的新URL给客户端，由客户端重新发起请求，状态码：301
break;
#重写完成后,停止对当前URL在当前location中后续的其它重写操作，而后直接跳转至重写规则配置块之后
的其它配置;结束循环，建议在location中使用
#适用于一个URL一次重写
last;
#重写完成后,停止对当前URI在当前location中后续的其它重写操作，而后对新的URL启动新一轮重写检查，
不建议在location中使用
#适用于一个URL多次重写，要注意避免出现超过十次以及URL重写后返回错误的给用户 	
```

###### redirect临时重定向:

![image-20240105135021970](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240105135021970.png)

```shell
server {
        listen 8888 ssl;
        ssl_certificate /data/package/nginx-server/secret/cn1.a.64ip.top.crt;
        ssl_certificate_key /data/package/nginx-server/secret/cn1.a.64ip.top.key;

        server_name cn1.a.64ip.top;
        root  /var/www/html;

        location ~ ^/ngd/ {
           root /var/www/html;
           
           # https://cn1.a.64ip.top/ngd -> https://cn1.a.64ip.top/test
           rewrite ^/ngd/(.*) /test1/$1 redirect;
        }
}
```

###### permanent永久重定向:

![image-20240105135337033](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240105135337033.png)

```shell
server {
        listen 8888 ssl;
        ssl_certificate /data/package/nginx-server/secret/cn1.a.64ip.top.crt;
        ssl_certificate_key /data/package/nginx-server/secret/cn1.a.64ip.top.key;

        server_name cn1.a.64ip.top;
        root  /var/www/html;

        location ~ ^/ngd/ {
           root /var/www/html;
           
           # https://cn1.a.64ip.top/ngd -> https://cn1.a.64ip.top/test
           rewrite ^/ngd/(.*) /test1/$1 permanent;
        }
}
```

###### last案例:

```shell
last：对某个location的URL匹配成功后,会停止当前location的后续rewrite规则，并结束当前location，然后将匹配生成的新URL跳转至其他location继续匹配，直到没有locatio可匹配后, 将最后一次location的数据返回给客户端.

# 配置
location /test2 {
       default_type text/plain;
       return 666 "new test2";
       #echo "new test2";
}
location /test1 {
     default_type text/plain;
      #return 999 "new test1";
      #echo "new test1";
     rewrite ^/test1/(.*) /test2/$1 last;
}
location /last {
     root /data/nginx;
     index index.html;
     rewrite ^/last/(.*) /test1/$1 last;
     rewrite ^/test1/(.*) /test2/$1 last; #如果第一条rewrite规则匹配成功则不执行本条，
否则执行本条rewrite规则。
}
   
    
#last访问测试：
[root@centos8 ~]#curl   -L   http://www.magedu.org/last/index.html
new test2 #会匹配多个location，直到最终全部匹配完成，返回最后一个location的匹配结果给客户
端。
```

###### break案例:

```shell
break: 当规则匹配后，rewirte执行后结束当前localtion，server中的其他location也不在进行规则匹配。


# 配置
   location /break {
      #return 666 "break";
     root /data/nginx;
     index index.html;
     rewrite ^/break/(.*) /test1/$1 break;  #break匹配成功后不再向下匹配，也不会跳转到
其他的location，即直接结束匹配并给客户端返回结果数据。
     rewrite ^/test1/(.*) /test2/$1 break;  #break不会匹配后面的rewrite规则也不匹配
location
   }
   location   /test1 {
     default_type text/plain;
      echo "new test1";
     return 999 "new test1";
   }
     location   /test2 {
     default_type text/plain;
      echo "new test2";
     return 666 "new test2";
   }
     
#创建资源路径：
[root@centos8 ~]# mkdir /data/nginx/break
[root@centos8 ~]# mkdir /data/nginx/test1
[root@centos8 ~]# mkdir /data/nginx/test2
[root@centos8 ~]# echo break > /data/nginx/break/index.html 
[root@centos8 ~]# echo test1 > /data/nginx/test1/index.html 
[root@centos8 ~]# echo test2 > /data/nginx/test2/index.html 
#break访问测试：注意下面的index.html必须加
[root@centos7 ~]#curl -i www.magedu.org/break/index.html 
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Thu, 08 Oct 2020 14:16:22 GMT
Content-Type: text/html
Content-Length: 6
Last-Modified: Thu, 08 Oct 2020 14:08:47 GMT
Connection: keep-alive
ETag: "5f7f1d6f-6"
Accept-Ranges: bytes
test1

#最终的结果不会超出break的所在的location而且不会继续匹配当前location后续的write规则，而且直接返回数据给客户端
```

## Haproxy:

![image-20240221160716913](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221160716913.png)

### 负载均衡简介:

![image-20240221161254566](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221161254566.png)

```shell
负载均衡：Load Balance，简称LB，是一种服务或基于硬件设备等实现的高可用反向代理技术，负载均
衡将特定的业务(web服务、网络流量等)分担给指定的一个或多个后端特定的服务器或设备，从而提高了
公司业务的并发处理能力、保证了业务的高可用性、方便了业务后期的水平动态扩展

阿里云SLB介绍 ：https://yq.aliyun.com/articles/1803
```

```shell
Web服务器的动态水平扩展	-->		对用户无感知
增加业务并发访问及处理能力 -->	  解决单服务器瓶颈问题
节约公网IP地址		   -->	   降低IT支出成本
隐藏内部服务器IP         -->	  提高内部服务器安全性
配置简单				-->		固定格式的配置文件
功能丰富				-->		支持四层和七层，支持动态下线主机
性能较强				-->		并发数万甚至数十万
```

### 市面常用负载均衡:

#### 四层调度:

```shell
#LVS技术特点:
	LVS是全球最流行的四层负载均衡开源软件，由章文嵩博士（当前阿里云产品技术负责人）在1998年5月创立，可以实现LINUX平台下的负载均衡。
    LVS是 基于linux netfilter框架实现（同iptables）的一个内核模块，名称为ipvs；其钩子函数分别HOOK在LOCAL_IN和FORWARD两个HOOK点,在内核中完成调度，流量不会进入用户空间。
    
#Nginx技术特点:
	nginx 在1.9版本之后支持TCP、UDP协议代理，nginx主要是做静态服务器，Nginx采用事件驱动方式能够处理大量的并发连接，因此也常用于四层代理中

#Envoy技术特点：
   envoy是一个现代化的高性能边缘服务代理，由CNCF维护，常见使用在微服务治理场景例如istio，面向云原生，支持多种功能、熔断、路由、重试、故障注入等功能
   
#Haproxy技术特点：
   haproxy是一个专用于负载均衡而生的代理服务，其支持多种的调度算法例如 hdr、hash、uri、权重、轮询、parm等等10多种算法，同样采用事件驱动模型，单进程模式下也有很出色的代理能力，很多构建高性能的站点通常都使用haproxy作为站点入站反向代理
```

#### 七层调度:

```shell
#haproxy
	haproxy 支持七层调度用于acl控制
#nginx
    nginx 支持七层调度支持使用location进行控制
#envoy
	envoy 支持七层调度通常面向云原生场景，支持细粒度的流量调度
```

### 应用场景:

```shell
   在企业生产环境中，每天会有很多的需求变更，比如增加服务器、新业务上线、url路由修改、域名配置等等，对于前端负载均衡设备来说，容易维护，复杂度低，是首选指标。在企业中，稳定压倒一切，与其搞得很复杂，经常出问题，不如做的简单和稳定。在企业中，90%以上的故障，来源于需求变更。可能是程序bug，也可能是人为故障，也可能是架构设计问题等。前端负载均衡设备为重中之重，在软件选型上一定充分考虑，能满足业务的前提下，尽可能降低复杂度，提高易维护性
```

### Haproxy简介:

![image-20240221163431815](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221163431815.png)

```shell
HAProxy是法国开发者 威利塔罗(Willy Tarreau) 在2000年使用C语言开发的一个开源软件，是一款具
备高并发(一万以上)、高性能的TCP和HTTP负载均衡器，支持基于cookie的持久性，自动故障切换，支
持正则表达式及web状态统计，目前最新LTS版本为2.8

Haproxy 拥有商业版本

# 支持功能特性
1. TCP 和 HTTP反向代理
2. SSL/TSL服务器
3. 可以针对HTTP请求添加cookie，进行路由后端服务器
4. 可平衡负载至后端服务器，并支持持久连接
5. 支持所有主服务器故障切换至备用服务器
6. 支持专用端口实现监控服务
7. 支持停止接受新连接请求，而不影响现有连接
8. 可以在双向添加，修改或删除HTTP报文首部
9. 响应报文压缩
10. 支持基于pattern实现连接请求的访问控制
11. 通过特定的URI为授权用户提供详细的状态信息

# 不具备的功能
正向代理	--	  squid，nginx
缓存代理	--	  varnish，nginx
web服务	 --	   nginx、tengine、apache、php、tomcat
UDP		   --	目前不支持UDP协议
单机性能	--	  相比LVS性能较差
```

### 常用配置需求:

####  layer 4 与 layer 7:

![image-20240221164753603](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221164753603.png)

```shell
四层：IP+PORT转发
七层：协议+内容交换

   四层负载设备中，把client发送的报文目标地址(原来是负载均衡设备的IP地址)，根据均衡设备设置的选择web服务器的规则选择对应的web服务器IP地址，这样client就可以直接跟此服务器建立TCP连接并发送数据，而四层负载自身不参与建立连接，而和LVS不同，haproxy是伪四层负载均衡，因为haproxy需要分别和前端客户端及后端服务器建立连接

   七层负载均衡服务器起了一个反向代理服务器的作用，服务器建立一次TCP连接要三次握手，而client要访问Web Server要先与七层负载设备进行三次握手后建立TCP连接，把要访问的报文信息发送给七层负载均衡；然后七层负载均衡再根据设置的均衡规则选择特定的 Web Server，然后通过三次握手与此台Web Server建立TCP连接，然后Web Server把需要的数据发送给七层负载均衡设备，负载均衡设备再把数据发送给client；所以，七层负载均衡设备起到了代理服务器的作用，七层代理需要和Client和后端服务器分别建立连接


```

##### 四层IP透传配置:

```shell
#haproxy 配置：
# 四层透传建议使用listen方式
# 四层透传仅支持TCP协议
listen http_nodes
 	bind  80
 	mode tcp
 	balance roundrobin
 	server web1 10.180.0.53:80 send-proxy check inter 3000 fall 3 rise 5 
 	#添加send-proxy
	#nginx 配置：在访问日志中通过变量$proxy_protocol_addr 记录透传过来的客户端IP


# nginx log配置获取真实的client访问IP 使用变量$proxy_protocol_addr
http {
		log_format main  '$remote_addr - $remote_user [$time_local] "$request"
"$proxy_protocol_addr"'
 		server {
   			listen    80 proxy_protocol; #启用此项，将无法直接访问此网站，只能通过四层代理
访问
   			server_name web01.com;
```

##### 七层IP透传:

```shell
   haproxy工作在七层的时候，也可以透传客户端真实IP至后端服务器
   haproxy发往后端主机的请求报文中添加“X-Forwarded-For"首部，其值为前端客户端的地址；用于
向后端主发送真实的客户端IP,配置实例如下:

    option forwardfor [ except <network> ] [ header <name> ] [ if-none ]
    	[ except <network> ]：请求报请来自此处指定的网络时不予添加此首部，如haproxy自身所在网络
    	[ header <name> ]：使用自定义的首部名称，而非“X-Forwarded-For"，示例：X-client
    	[ if-none ] 如果没有首部才添加首部，如果有使用默认值
    	   	
# 配置实例
defaults
    #此为默认值,首部字段默认为：X-Forwarded-For
    option forwardfor 
    #或者自定义首部,如:X-client
    # except 表示排除
    option forwardfor except 127.0.0.0/8 header X-client
listen web_host
    bind 10.0.0.7:80
    mode http
    log global
    balance random
    server web1 10.0.0.17:80 weight 1 check inter 3000 fall 2 rise 5
    server web2 10.0.0.27:80 weight 1 check inter 3000 fall 2 rise 5
    
#apache 配置：
	LogFormat "%{X-Forwarded-For}i %a %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"% {User-Agent}i\"" combined
#nginx 日志格式：
	$proxy_add_x_forwarded_for：包括客户端IP和中间经过的所有代理的IP
	$http_x_forwarded_For：只有客户端IP
	log_format main  '"$proxy_add_x_forwarded_for" - $remote_user [$time_local]
"$request" ' '$status $body_bytes_sent "$http_referer" ' '"$http_user_agent" $http_x_forwarded_For';
          
```

#### haproxy会话保持:

##### hash方式:

###### hash对象:

![image-20240221154229129](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221154229129.png)

```shell
hash:
    请求对象做hash计算，计算的结果会得到一个固定长度、固定值的随机字符串，常见算法MD5、SHA-1等
```

###### 一致性hash:

![image-20240221154351596](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221154351596.png)

![image-20240221154735616](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221154735616.png)

```shell
一致性hash: 
  2^32-1进行取模形成一个环，当服务器的总权重发生变化时，对调度结果影响是局部的，不会引起大的变动，
hash（o）mod n ，该hash算法是动态的，支持使用 socat等工具进行在线权重调整，支持慢启动
  
# 计算方式  
1、key1=hash(source_ip)%(2^32) [0---4294967295]
2、keyA=hash(后端服务器虚拟ip)%(2^32)
3、将key1和keyA都放在hash环上，将用户请求调度到离key1最近的keyA对应的后端服务器
```

###### hash-type选项:

```shell
hash-type 主要用于给balance 算法指定一个hash类型，从而决定了如果根据请求内容或源来选择后端的服务器。

# haproxy支持类型
  1. consistent	一致性hash
  2. map-based  对source地址进行hash计算，再基于服务器总权重的取模，最终结果决定将此
请求转发至对应的后端服务器。此方法是静态的，即不支持在线调整权重，不支持慢启动，可实现对后
端服务器均衡调度。缺点是当服务器的总权重发生变化时，即有服务器上线或下线，都会因总权重发生
变化而导致调度结果整体改变，hash-type 指定的默认值为此算法
```

###### source方式:

```shell
source 采用的hash方式将源地址对后端的server取模方式进行会话粘性绑定，缺点当server挂了一台后所有的hash结果都会失效，因此在使用时可以添加hash-type选项来使用一致性hash算法。


#配置
backend http-server
  mode http
  #cookie WEBSERVER rewrite 
  balance roundrobin
  balance source
  hash-type consistent
  server web01 127.0.0.1:80 check inter 3 fall 3 rise 3
  server web02 127.0.0.1:81 check inter 3 fall 3 rise 3



```

###### hdr方式:

```shell
hdr()方法可以根据request header中的关键字进行hash

# 通过客户浏览器方式
hdr(User-Agent)
# 通过主机名称
hdr(Host)


# 配置样例
backend http-server
  mode http
  #cookie WEBSERVER rewrite 
  balance roundrobin
  balance hdr(User-Agent)
  hash-type consistent
  server web01 127.0.0.1:80 check inter 3 fall 3 rise 3
  server web02 127.0.0.1:81 check inter 3 fall 3 rise 3
```



##### cookie方式:

```shell
cookie value：为当前server指定cookie值，实现基于cookie的会话黏性，相对于基于 source 地址
hash 调度算法对客户端的粒度更精准，但同时也加大了haproxy负载，目前此模式使用较少， 已经被session共享服务器代替.

# 注意
  不支持tcp mode模式
  
# 配置方式
cookie <name> <参数>

# 可配置区域
defaults、listen、backend

# 参数
name:		定义返回给client端的cookie名称，应该保持唯一性不能冲突，下次client在请求将会带着cooki来到haporxy因此会通过cookie的value给会话做持久绑定
rewrite: 	如果cookie value 存在将会覆盖
insert： 	向响应报文中插入cookie value
indirect: 	如果cookie已经被设置将不会在设置cookie
```

###### insert方式:

**cookie 绑定成功**

![image-20240221153150032](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221153150032.png)

```shell
backend http-server
  mode http
  cookie WEBSERVER insert
  balance roundrobin
  server web01 127.0.0.1:80 check inter 3 fall 3 rise 3 cookie web01
  server web02 127.0.0.1:81 check inter 3 fall 3 rise 3 cookie web02
```

###### indirect方式:

**当定义了cookie name 时将不会在设置对应value**

![image-20240221153004280](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221153004280.png)

```shell
backend http-server
  mode http
  cookie WEBSERVER indirect
  balance roundrobin
  server web01 127.0.0.1:80 check inter 3 fall 3 rise 3 cookie web01
  server web02 127.0.0.1:81 check inter 3 fall 3 rise 3 cookie web02
```

#### haproxy报文修改:

**报文流程**

![image-20240221173820964](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221173820964.png)

**可配置区域**

![image-20240221180343033](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221180343033.png)

```shell
Haproxy 一手托2家,在7层模式下，haproxy是可以对每个阶段的请求报文做报文修改，新增、删除、等操作

# request操作
# 插入一个新的header
http-request add-header <name> <fmt> [ { if | unless } <condition> ]
# 删除一个header
http-request del-header <name> [ -m <meth> ] [ { if | unless } <condition> ]
# 
```

##### backend修改报文:

###### 插入一个新的header:

```shell
# 需求
  haproxy在向后端发起连接时新增一个header首部"add: new"
# 配置如下
# 首先需要明确haproxy调用后端server是发生在backend区域完成的，因此需要在backend区域加上add-header参数

backend http-server
  mode http
  #cookie WEBSERVER rewrite 
  balance roundrobin
  balance hdr(User-Agent)
  hash-type consistent
  # 新增首部信息
  http-request add-header add new
  server web01 127.0.0.1:80
  server web02 127.0.0.1:81 check inter 3 fall 3 rise 3


```

**抓包backend server调用**

![image-20240221181214356](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221181214356.png)

###### 删除一个header:



```shell
# 需求
  haproxy 在请求backend server时需要删除add header首部
  
# 配置如下
backend http-server
  mode http
  #cookie WEBSERVER rewrite 
  balance roundrobin 
  balance hdr(User-Agent)
  hash-type consistent
  http-request add-header add new
  http-request add-header test 123
  # 删除header add
  http-request del-header add
  server web01 127.0.0.1:80 
  server web02 127.0.0.1:81 check inter 3 fall 3 rise 3
```

**删除后抓包截图**

![image-20240221182814091](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221182814091.png)

#### haproxy开启压缩:

**未开启压缩时**

![image-20240221142409338](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221142409338.png)

**开启压缩**

![image-20240221143419365](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240221143419365.png)

```shell
# 选项:
# 开启HTTP压缩功能
# 支持配置区域 defaults、frontend、backend、listen
# 配置语法 compression <argument> <算法>
compression algo <algorithm> ...
compression algo-req <algorithm>
compression algo-res <algorithm>
compression type <mime type> ...

# arguments
algo： 			响应client压缩
algo-req:	 
algo-res:		 
algo-type：		指定haproxy要压缩的类型文件

# 支持的算法
gzip                                      #常用的压缩方式，与各浏览器兼容较好
deflate                                   #有些浏览器不支持
raw-deflate                               #新式的压缩方式

# 配置案例
defaults
  compression algo gzip
  compression type text/html text/plain text/css text/xml text/javascript application/javascript
```

#### haproxy开启状态页:

```shell
# haproxy 默认自带当前haproxy工作状态统计页面，里面包含了当前haproxy工作连接数、后端server运行状态、同时也可以做上线、下线操作。


# 开启stat状态页面

# 定义配置
listen stats
  mode http
  bind 0.0.0.0:8124
  stats enable
  stats uri /haproxy?stats
  stats realm "Haproxy 监控页面"
  stats auth admin1:123456
  stats refresh 5
  stats admin if TRUE	

```



#### haproxy开启日志记录:

```shell
# haproxy 的日志记录需要借助于系统的syslog功能

# 开启syslog并配置
vim /etc/rsyslog.conf
# Provides UDP syslog reception
$ModLoad imudp
$UDPServerRun 514

local2.*	/var/log/haproxy/haproxy.log

# 创建日志目录
mkdir /var/log/haproxy 
chown haproxy.haproxy /var/log/haproxy

# 重启rsyslog
systemctl daemon-reload
systemctl restart rsyslog

# haproxy 配置
global
  maxconn 65535
  maxsslconn 65535
  daemon
  user haproxy
  group haproxy
  chroot /data/haproxy/chroot
  spread-checks 3
  maxzlibmem 6348

defaults
  log 127.0.0.1:514 local5 info
```

#### client 真实IP透传:

```shell
# 将真实的client端IP透传到后端server，如果不配置后端server将都获取haproxy的ip地址


# 配置参数
# backend 、frontend、default、listend
  option forwardfor [ except <network> ] [ header <name> ] [ if-none ]



# 默认标准配置
backend http80
  option forwardfor 



# 自定义header配置样例
frontend http80-frontend
  # except 表示排除某个IP地址的“X-Forwarded-For”IP记录
  option forwardfor except 10.180.0.5
  mode http
  bind :8111
  use_backend http80
  
backend http80
  balance roundrobin
  fullconn 1000
  mode http
  # 自定义首部
  option forwardfor header X-client
  # 排除不能加到backend内不然会不生效或者不透传
  #option forwardfor except 127.0.0.1
  server web01 10.180.0.56:80 check fall 3 inter 3 rise 3
  server web02 10.180.0.88:8123 check fall 3 inter 3 rise 3


# httpd conf配置
vim /etc/httpd/conf/httpd.conf
   
   LogFormat "\"%{X-client}i\" %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
```

##### http配置透传IP:

```shell
# 修改配置
vim /etc/httpd/conf/httpd.conf
   
   LogFormat "\"%{X-client}i\" %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined


# 重启
systemctl restart httpd
```

### 常用配置选项:

```shell
# haproxy 配置文件分为2大区域“global”、“proxies”，每个区域的功能各不相同

global			// 全局配置参数区域、性能优化配置、连接数配置等
# proxies 段
defaults			// 为proxies区域提供默认配置参数，如果proxies自定义了参数与defaults区域相同proxies区域的优先级更高
		
frontend		// 面向client端的连接器配置段
backend			// 面向后端server连接配置段
listend			// 合并了frontend和backend俩个配置段落
```

#### global配置参数:

```shell
# 安全配置
user haproxy						// haproxy进程执行用户
group haproxy						// haproxy进程执行用户组
chroot /data/haproxy/chroot			// 防止进程漏洞被攻击时获取系统权限，默认将进程禁锢在配置目录内

# 性能配置
maxconn 65535						// haproxy 面向client最大连接并发数
maxsslconn 65535					// haproxy 面向Tls client最大连接并发数
spread-checks 3						// haproxy 在健康状态检测时采用分散散列方式进行请求，而不是一次性对所有的server做发送检测命令，有效降低服务器负载，配置3表示haproxy尝试在3秒内分散发送健康状态检测。
maxzlibmem 6348						// haproxy 支持数据包压缩响应功能，此配置表示在压缩时使用内存的大小，官方建议 total Mem / 10
nbproc 4							// haproxy 默认单进程模型，也可以调整多进程工作方式，根据CPU核心数量配置
cpu-map	1 0							// 将进程绑定到指定的cpu之上运行防止做切换多进程模式下提高性能
option tcpka						// 在高并发场景可以开启tcp连接复用以减少资源占用
timeout client-fin 15				// 客户端发送关闭连接haproxy 最大等待时间，防止连接被一直不释放导致端口被使用尽

# 运行模式
daemon								// haproxy 配置工作在后台运行

# 控制信息
stats socket /var/run/haproxy.sockt mode 600 level admin		// 可以通过此socket做上下线、状态信息查看等

```

#### proxiex配置参数:

###### defaults配置参数:

```shell
# defaults 提供一些默认行为和参数，以适用于所有的后端服务器
mode http|tcp						// 指定默认情况下后端server工作协议
timeout connect 10s					// 设置连接超时时间即客户端于服务器建立连接最大等待时间
timeout client 30s					// 设置客户端超时时间，客户端在连接haproxy后俩次数据包发送的最大等待时间
timeout server 30s					// 设置haproxy于后端server数据包最大等待时间
timeout tunnel 1h					// TCP模式下超时时间
option httplog						// 使haproxy记录http请求、响应详细信息
option tcplog						// 使haproxy记录tcp请求、响应日志记录
option http-server-close			// 在客户端请求完成后关闭后端server的连接
option forwardfor					// 向后端server传输真实的客户端IP地址
balance								// 指定调度算法

```

###### backend配置参数:

```shell
# backend 对接后端的server
mode								// 指定工作协议
balance								// 调度算法
timeout connect						// haproxy 与server建立连接超时时间
timeout server						// haproxy 与server传输数据超时时间
option httpchk GET /health		    // 启动对后端server http健康状态检测
http-check expect status 200		// http状态检测时期望获得的响应码
server								// 定义后端server地址
http-request set-header				// 自定义新增header信息发送到后端server
```

###### frontend配置参数:

```shell
# frontend 定义前端配置接收客户端请求
bind								// 监听IP端口
mode								// 工作模式
timeout client						// 客户端连接超时时间，数据包发送超时时间
timeout http-request				// 设置客户端请求超时时间
default_backend						// 定义默认使用的backend组通常配合ACL做控制
acl									// 定义访问控制列表，根据匹配规则做控制操作
use_backend							// 定义当前frontend使用的server backend
option forwardfor					// 透传真实客户端请求地址
option http-keep-alive				// 开启持久连接

```

### 调度算法:

#### 静态算法:

```shell
# 静态算法在运行时不会动态的去进行修改，按照特定调度算法进行调度
# Backend is using a static LB algorithm and only accepts weights '0%' and '100%'.
static-rr:	 基于权重的方式进行调度，运行过程中不能通过socat方式进行修改不会生效
first:		会根据ID最小的数字来选择一台server当这个server 连接数达到上限时才会使用其他节点
```

#### 动态算法:

```shell
# 动态算法是服务进程在运行时根据运行情况进行调度
lessconn：  根据后端server连接数还进行最少连接调度，适用于非长连接模式请求。
roundrobin  根据权重进行调度，如果权重一致那么将安顺序进行依次轮叫。
source:		根据client原地址IP进行调度。
uri:		该算法对URI的左侧部分进行散列处理，hash-type consistent 表示使用一致性hash算法。
url_param	根据请求携带的参数进行hash调度 hash-type consistent 表示使用一致性hash算法。
hdr			根据指定的请求首部信息进行hash调度 hash-type consistent 表示使用一致性hash算法。
random		haproxy会生成一个随机的数字作为hash key来随机调度到后端的server之上。
	# 注意
	random 和 roundrobind都是随机调度，但是本质上是不通的roundrobin是固定方式进行轮叫，random
	是根据随机数做hash每个请求都是不固定的调度到某个节点之上，二者都支持权重动态修改。

```

#### 算法总结:

```shell
#静态
static-rr--------->tcp/http 
first------------->tcp/http 

#动态
roundrobin-------->tcp/http
leastconn--------->tcp/http
random------------>tcp/http

#以下静态和动态取决于hash_type是否consistent
source------------>tcp/http
Uri--------------->http
url_param--------->http  
hdr--------------->http
rdp-cookie-------->tcp
```



### Haproxy 管理工具:

#### socat工具:

```shell
    对服务器动态权重和其它状态可以利用 socat工具进行调整，Socat 是 Linux 下的一个多功能的网络工具，名字来由是Socket CAT，相当于netCAT的增强版.Socat 的主要特点就是在两个数据流之间建立双向通道，且支持众多协议和链接方式。如 IP、TCP、 UDP、IPv6、Socket文件等
    
范例：利用工具socat 对服务器动态权重调整
[root@centos7 ~]#yum -y install socat
#查看帮助
[root@centos7 ~]#socat -h
[root@centos7 ~]#echo "help" | socat stdio /var/lib/haproxy/haproxy.sock
Unknown command. Please enter one of the following commands only :
help      : this message
prompt     : toggle interactive mode with prompt
quit      : disconnect
show tls-keys [id|*]: show tls keys references or dump tls ticket keys when id
specified
 set ssl tls-key [id|keyfile] <tlskey>: set the next TLS key for the <id> or
<keyfile> listener to <tlskey>
 set ssl cert <certfile> <payload> : replace a certificate file
commit ssl cert <certfile> : commit a certificate file
abort ssl cert <certfile> : abort a transaction for a certificate file
show sess [id] : report the list of current sessions or dump this session
shutdown session : kill a specific session
shutdown sessions server : kill sessions on a server
 clear counters : clear max statistics counters (add 'all' for all counters)
show info   : report information about the running process
[desc|json|typed]*
show stat   : report counters for each proxy and server [desc|json|typed]*
show schema json : report schema used for stats
disable agent : disable agent checks (use 'set server' instead)
disable health : disable health checks (use 'set server' instead)
disable server : disable a server for maintenance (use 'set server' instead) #
禁用服务器
enable agent  : enable agent checks (use 'set server' instead)
enable health : enable health checks (use 'set server' instead)
enable server : enable a disabled server (use 'set server' instead)  #启用服务
器
 set maxconn server : change a server's maxconn setting
 set server   : change a server's state, weight or address      #设置服务
器
 get weight   : report a server's current weight
 set weight   : change a server's weight (deprecated)
show startup-logs : report logs emitted during HAProxy startup
show peers [peers section]: dump some information about all the peers or this
peers section
 set maxconn global : change the per-process maxconn setting
 set rate-limit : change a rate limiting value
 set severity-output [none|number|string] : set presence of severity level in
feedback information
 set timeout  : change a timeout setting
show env [var] : dump environment variables known to the process
show cli sockets : dump list of cli sockets
show cli level  : display the level of the current CLI session
show fd [num] : dump list of file descriptors in use
 show activity : show per-thread activity stats (for support/developers)
operator    : lower the level of the current CLI session to operator
user      : lower the level of the current CLI session to user
 clear table  : remove an entry from a table
 set table [id] : update or create a table entry's data
show table [id]: report table usage stats or dump this table's contents
disable frontend : temporarily disable specific frontend
enable frontend : re-enable specific frontend
 set maxconn frontend : change a frontend's maxconn setting
show servers state [id]: dump volatile server information (for backend <id>)
show backend  : list backends in the current running config
shutdown frontend : stop a specific frontend
 set dynamic-cookie-key backend : change a backend secret key for dynamic
cookies
enable dynamic-cookie backend : enable dynamic cookies on a specific backend
disable dynamic-cookie backend : disable dynamic cookies on a specific backend
show errors  : report last request and response errors for each proxy
show resolvers [id]: dumps counters from all resolvers section and
          associated name servers
show cache   : show cache status
add acl    : add acl entry
 clear acl <id> : clear the content of this acl
del acl    : delete acl entry
 get acl    : report the patterns matching a sample for an ACL
show acl [id] : report available acls or dump an acl's contents
add map    : add map entry
 clear map <id> : clear the content of this map
del map    : delete map entry
 get map    : report the keys and values matching a sample for a map
 set map    : modify map entry
show map [id] : report available maps or dump a map's contents
trace <module> [cmd [args...]] : manage live tracing
show trace [<module>] : show live tracing state
show threads  : show some threads debugging information
show pools   : report information about the memory pools usage
show events [<sink>] : show event sink state
show profiling : show CPU profiling options
 set profiling : enable/disable CPU profiling
 
 
 # 查看haproxy工作状态
[root@centos7 ~]#echo "show info" | socat stdio /var/lib/haproxy/haproxy.sock
Name: HAProxy
Version: 2.1.3
Release_date: 2020/02/12
Nbthread: 4
Nbproc: 1
Process_num: 1
Pid: 2279
Uptime: 0d 0h46m07s
Uptime_sec: 2767
Memmax_MB: 0
PoolAlloc_MB: 0
PoolUsed_MB: 0
PoolFailed: 0
Ulimit-n: 200041
Maxsock: 200041
Maxconn: 100000
Hard_maxconn: 100000
CurrConns: 0
CumConns: 1
CumReq: 1
MaxSslConns: 0
CurrSslConns: 0
CumSslConns: 0
Maxpipes: 0
PipesUsed: 0
PipesFree: 0
ConnRate: 0
ConnRateLimit: 0
MaxConnRate: 0
SessRate: 0
SessRateLimit: 0
MaxSessRate: 0
SslRate: 0
SslRateLimit: 0
MaxSslRate: 0
SslFrontendKeyRate: 0
SslFrontendMaxKeyRate: 0
SslFrontendSessionReuse_pct: 0
SslBackendKeyRate: 0
SslBackendMaxKeyRate: 0
SslCacheLookups: 0
SslCacheMisses: 0
CompressBpsIn: 0
CompressBpsOut: 0
CompressBpsRateLim: 0
ZlibMemUsage: 0
MaxZlibMemUsage: 0
Tasks: 19
Run_queue: 1
Idle_pct: 100
node: centos7.wangxiaochun.com
Stopping: 0
Jobs: 7
Unstoppable Jobs: 0
Listeners: 6
ActivePeers: 0
ConnectedPeers: 0
DroppedLogs: 0
BusyPolling: 0
FailedResolutions: 0
TotalBytesOut: 0
BytesOutRate: 0
DebugCommandsIssued: 0
[root@centos7 ~]#cat /etc/haproxy/haproxy.cfg
......
listen magedu-test-80
bind :81,:82
mode http
server web1 10.0.0.17:80 check inter 3000 fall 3 rise 5
server web2 10.0.0.27:80 check weight 3 
......



# 查看backend server运行状态
[root@centos7 ~]#echo "show servers state" | socat stdio
/var/lib/haproxy/haproxy.sock
1
# be_id be_name srv_id srv_name srv_addr srv_op_state srv_admin_state srv_uweight
srv_iweight srv_time_since_last_change srv_check_status srv_check_result
srv_check_health srv_check_state srv_agent_state bk_f_forced_id srv_f_forced_id
srv_fqdn srv_port srvrecord
2 magedu-test-80 1 web1 10.0.0.17 2 0 2 1 812 6 3 7 6 0 0 0 - 80 -
2 magedu-test-80 2 web2 10.0.0.27 2 0 2 3 812 6 3 4 6 0 0 0 - 80 -
4 web_port 1 web1 127.0.0.1 0 0 1 1 810 8 2 0 6 0 0 0 - 8080 -


# 热修改backend server权重
[root@centos7 ~]#echo "get weight magedu-test-80/web2" | socat stdio
/var/lib/haproxy/haproxy.sock
3 (initial 3)
#修改weight，注意只针对单进程有效
[root@centos7 ~]#echo "set weight magedu-test-80/web2 2" | socat stdio
/var/lib/haproxy/haproxy.sock
[root@centos7 ~]#echo "get weight magedu-test-80/web2" | socat stdio
/var/lib/haproxy/haproxy.sock
2 (initial 3)


#将后端服务器禁用，注意只针对单进程有效
[root@centos7 ~]#echo "disable server magedu-test-80/web2" | socat stdio
/var/lib/haproxy/haproxy.sock

#启用后端服务器
[root@centos7 ~]#echo "enable server magedu-test-80/web2" | socat stdio
/var/lib/haproxy/haproxy.sock

#将后端服务器软下线，即weight设为0
[root@centos7 ~]#echo "set weight magedu-test-80/web1 0" | socat stdio
/var/lib/haproxy/haproxy.sock

#针对haproxy的多进程,将后端服务器禁用
[root@centos7 ~]#vim /etc/haproxy/haproxy.cfg
......
stats socket /var/lib/haproxy/haproxy1.sock mode 600 level admin process 1 #绑定第
1个进程和socket文件
stats socket /var/lib/haproxy/haproxy2.sock mode 600 level admin process 2 #绑定第
2个进程和socket文件
nbproc 2
.....
[root@centos7 ~]#echo "disable server magedu-test-80/web2" | socat stdio
/var/lib/haproxy/haproxy1.sock
[root@centos7 ~]#echo "disable server magedu-test-80/web2" | socat stdio
/var/lib/haproxy/haproxy2.sock
[root@haproxy ~]#for i in {1..2};do echo "set weight magedu-test-80/web$i 10" |
socat stdio /var/lib/haproxy/haproxy$i.sock;done



#如果静态算法，如:static-rr，可以更改weight为0或1，但不支持动态更改weight为其它值，否则会提
示下面信息
[root@centos7 ~]#echo "set weight magedu-test-80/web1 0" | socat stdio
/var/lib/haproxy/haproxy.sock
范例: 上线和下线后端服务器脚本
4.1.2 static-rr
static-rr：基于权重的轮询调度，不支持运行时利用socat进行权重的动态调整(只支持0和1,不支持其它
值)及后端服务器慢启动，其后端主机数量没有限制，相当于LVS中的 wrr
4.1.3 first
first：根据服务器在列表中的位置，自上而下进行调度，但是其只会当第一台服务器的连接数达到上
限，新请求才会分配给下一台服务，因此会忽略服务器的权重设置，此方式使用较少
不支持用socat进行动态修改权重,可以设置0和1,可以设置其它值但无效
[root@centos7 ~]#echo "set weight magedu-test-80/web1 1" | socat stdio
/var/lib/haproxy/haproxy.sock
[root@centos7 ~]#echo "set weight magedu-test-80/web1 2" | socat stdio
/var/lib/haproxy/haproxy.sock
Backend is using a static LB algorithm and only accepts weights '0%' and '100%'.



# 上下线脚本
[root@centos7 ~]#cat haproyx_host_up_down.sh
. /etc/init.d/functions
case $1 in
up)
  echo "set weight magedu-m42-web-80/$2 1" | socat stdio
/var/lib/haproxy/haproxy.sock
 [ $? -eq 0 ] && action "$2 is up"
 ;;
down)
  echo "set weight magedu-m42-web-80/$2 0" | socat stdio
/var/lib/haproxy/haproxy.sock
 [ $? -eq 0 ] && action "$2 is down"
 ;;
*)
  echo "Usage: `basename $0` up|down IP"
 ;;
esac
```

## 高可用性

```shell
# 负载均衡集群
  流量在多节点调度可以做健康状态检测当某节点失败可以正常进行流量调度
# 高可用集群 
  当主节点宕机后仍然拥有一台节点可以正常提供服务
# 高性能集群
```

### keepalived

#### 简述:

```shell
   Keepalived 是一个用 C 语言编写的路由软件。该项目的主要目标是为 Linux 系统和基于 Linux 的基础设施提供简单而强大的负载均衡和高可用性设施。负载均衡框架依赖于众所周知且广泛使用的Linux 虚拟服务器 (IPVS) 内核模块来提供第 4 层负载均衡.
   
   1. 通过vrrp路由来实现故障转移
   2. 主节点会通过组播或单播方式进行消息投递

```

#### VRRP协议:

```shell
# vrrp 协议主要是为了实现单点静态路由器不能高可用问题

# vrrp组成结构
	1. vrrp路由器:  运行了vrrp D的程序
	2. vrrp虚拟路由器: 0-255,是一个虚拟逻辑路由器
	3. Master: 通过vrrp竞争选举出来的主节点
	4. backeup: 竞争失败节点做matser节点的备用机会实时接收master状态
	
# 工作机制
  vrrp通过竞选协议来实现虚拟路由器功能，全部通过多播（224.0.0.18）或单播方式进行发送，
  虚拟路由器ID通常在0-255区间（虚拟路由ID+VIP）组成，在虚拟路由器中只有master节点在不
  停发送vrrp组播数据包，backup角色在能接收到vrrp组播包后不会进行角色强占，选举是通过优
  先级配置来产生(priority)，抢占速度<1s内完成以保证服务连续性，vrrp发送的数据包也是加密
  形式。
```

#### keepalived设计于实现:

![keepalived software design](C:\Users\THINKPAD\Desktop\学习文档\图片\watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTIzMjQ3OTg=,size_16,color_FFFFFF,t_70)

```shell
# keepalived 采用了多进程模式，每个进程负责不同的服务功能

core： 			keepalived核心程序，全局配置解析、管理进程启动

vrrp:  			实现了vrrp d 程序代码用来实现vrrp协议

check: 			keepalived的health checker子进程的目录 包括了所有的健康检查方式以及对应的配置的解析， LVS的配置解析也在这个里面

SMTP: 			实现了邮件通知机制

IPVS: 			keepalived 可以直接生成ipvs规则就是调用此模块生成

control plane:  负责主配置文件加载解析

watchDog:		用来监控keepalived进程运行状态，当进程出现异常时会采取一些特定工作措施例如重启启动进程
```

#### keepalived部署:



#### keepalived配置讲解:

```shell
# keepalived 配置文件分为三个区域

1. 全局区域(global)
2. vrrp配置区域（vrrp_instance）
3. lvs配置区域(virtual_server)


```

##### global空间:

```shell
# 全局定义主要设置keepalived的通知机制和标识：



glabal_defs:
	#keepalived支持运行修改配置文件，当热修改时配置文件会保存在此目录从而下次启动时配置仍然是最新的，此目录必须手动创建。
	config_save_dir: path	
	# keepalived监视进程列表如果设置的进程出现了故障会自动进行重启，属于优化参数例如不需要ipvs功能可以将其取消，从而来降低keepalived服务工作负载。
    process_names:	process_name
        默认值：process_names: keepalived, keepalived_vrrp, keepalived_ipvs, keepalived_bfd
	# keepalived在启动时执行的脚本或者命令，主要是做启动前优化动作
	startup_script：	SCRIPT_NAME [username [groupname]]  
	# 启动脚本执行超时时间
	startup_script_timeout: SECONDS    # range [1,1000]
	# keepalived在关闭时执行的脚本
	shutdown_script	CRIPT_NAME [username [groupname]]
	shutdown_script_timeout SECONDS   # range [1,1000]
	# 配置邮件接收地址
	notification_email {
               admin@example1.com
               ...
           }
    # 标题电子邮件地址 
    notification_email_from admin@example.com
    # 邮件smtp地址
	smtp_server 127.0.0.1 [<PORT>]
	# 在邮件消息中使用的名称标题
	smtp_helo_name <STRING>
	# smtp服务器连接超时时间
	smtp_connect_timeout 30
	# keepalived运行机器唯一标识默认使用主机名
	router_id my_hostname
	# ipv4下默认使用的组播地址
	vrrp_mcast_group4 224.0.0.18
	# ipv6下默认使用的组播地址
	vrrp_mcast_group6 ff02::12
	# vrrp发送消息的网卡名称
	default_interface eth0

```

##### vrrp空间:

```shell

vrrp_instance inside_network {
	state MASTER
	interface eth0
	dont_track_primary
	track_interface {
		eth0
		eth1
	}
	mcast_src_ip <IPADDR>
	garp_master_delay 10
	virtual_router_id 51
	priority 100
	advert_int 1
	authentication {
		auth_type PASS
		autp-pass 1234
	}
	virtual_ipaddress {
		#<IPADDR>/<MASK>brd<IPADDR>dev<STRING>scope<SC OPT>label<LABEL>
		192.168.200.17/24 dev eth1
		192.168.200.18/24 dev eth2 label eth2:1
	}
	virtual_routes {
		#src<IPADDR>[to] <IPADDR>/<MASK>via lgw<IPADDR>dev<STRING>scope<SCOPE>
		src 192.168.100. 1 to 192.168.109.0/24 via 192.168.200.254 dev eth1
		192.168.110.0/24 via 192.168.200.254 dev eth1
		192.168.111.0/24 dev eth2
		192.168.112.0/24 via 192.168.100. 254
	}
	nopreempt
	preemtp_delay 300
	debug
}




```


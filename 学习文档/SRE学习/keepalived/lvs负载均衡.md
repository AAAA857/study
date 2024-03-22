# LVS

## 负载均衡产品:

```shell
  
# 负载均衡
  网络中常见的负载均衡主要分为两种：一种是通过硬件来进行进行，常见的硬件有比较昂贵的NetScaler、F5、Radware和Array等商用的负载均衡器，也有类似于LVS、Nginx、HAproxy的基于Linux的开源的负载均衡策略。

# 硬件设备
  商用负载均衡里面NetScaler从效果上比F5的效率上更高。对于负载均衡器来说，不过商用负载均衡由于可以建立在四~七层 协议之上，因此适用 面更广所以有其不可替代性，他的优点就是有专业的维护团队来对这些服务进行维护、缺点就是花销太大，所以对于规模较小的网络服务来说暂时还没有需要使用。

# 软件设备
  负载均衡的方式是通过软件：比较常见的有LVS、Nginx、HAproxy等，其中LVS是建立在四层协议上面的，而另外Nginx和HAproxy是建立在七层协议之上的，下面分别介绍关于

Nginx的特点是：

    1、工作在网络的7层之上，可以针对http应用做一些分流的策略，比如针对域名、目录结构；
    2、Nginx对网络的依赖比较小；
    3、Nginx安装和配置比较简单，测试起来比较方便；
    4、也可以承担高的负载压力且稳定，一般能支撑超过1万次的并发；
    5、Nginx可以通过端口检测到服务器内部的故障，比如根据服务器处理网页返回的状态码、超时等等，并且会把返回错误的请求重新提交到另一个节点，不过其中缺点就是不支持url来检测；
    6、Nginx对请求的异步处理可以帮助节点服务器减轻负载；
    7、Nginx能支持http和Email，这样就在适用范围上面小很多；
    8、不支持Session的保持、对Big request header的支持不是很好，另外默认的只有Round-robin和IP-hash两种负载均衡算法。


HAProxy的特点是：

    1、HAProxy是工作在网络7层之上。
    2、能够补充Nginx的一些缺点比如Session的保持，Cookie的引导等工作
    3、支持url检测后端的服务器出问题的检测会有很好的帮助。
    4、更多的负载均衡策略比如：动态加权轮循(Dynamic Round Robin)，加权源地址哈希(Weighted Source Hash)，加权URL哈希和加权参数哈希(Weighted Parameter Hash)已经实现
    5、单纯从效率上来讲HAProxy更会比Nginx有更出色的负载均衡速度。
    6、HAProxy可以对Mysql进行负载均衡，对后端的DB节点进行检测和负载均衡。 

```

**软负载均衡器性能对比**

![img](C:\Users\THINKPAD\Desktop\keepalived\负载均衡设备性能对比.png)





## lvs简述:

```shell
# 背景简述
   LVS是Linux Virtual Server的简称，也就是Linux虚拟服务器, 用现在的观点来看就是个4层（传输层tcp/udp）的负责均衡器。 它是一个由章文嵩博士发起的自由软件项目。
   
   官方站点：www.linuxvirtualserver.org
   
   现在LVS已经是 Linux标准内核的一部分，在Linux2.4内核以前，使用LVS时必须要重新编译内核以支持LVS功能模块，但是从Linux2.4内核以后，已经完全内置了LVS的各个功能模块，无需给内核打任何补丁，可以直接使用LVS提供的各种功能。
   
   LVS技术要达到的目标是：通过LVS提供的负载均衡技术和Linux操作系统实现一个高性能、高可用的服务器群集，它具有良好可靠性、可扩展性和可操作性。从而以低廉的成本实现最优的服务性能。
   
   
   
# 功能特性
    1、抗负载能力强、是工作在网络4层之上仅作分发之用，没有流量的产生；
    2、配置性比较低，这是一个缺点也是一个优点，因为没有可太多配置的东西，所以并不需要太多接触，大大减少了人为出错的几率；
    3、工作稳定，自身有完整的双机热备方案；
    4、无流量，保证了均衡器IO的性能不会收到大流量的影响；
    5、应用范围比较广，可以对所有应用做负载均衡；
    
# 适用环境
  # director
  LVS对前端Director Server目前仅支持Linux和FreeBSD系统，但是支持大多数的TCP和UDP协议，支持TCP协议的应用有： HTTP，HTTPS ，FTP，SMTP，，POP3，IMAP4，PROXY，LDAP，SSMTP 等等。支持UDP协议的应用有：DNS，NTP，ICP，视频、音频流播放协议等。
  # real server
  LVS对Real Server的操作系统没有任何限制，Real Server可运行在任何支持TCP/IP的操作系统上，包括Linux，各种Unix（如FreeBSD、Sun Solaris、HP Unix等），Mac/OS和Windows等。
  
# 缺点
 1. lvs的几种架构均对设备网络需要一定要求来实现
```

## lvs工作原理:

```shell
# 工作模式
  LVS的IP负载均衡技术是通过IPVS模块来实现的，IPVS是LVS集群系统的核心软件，它的主要作用是：安装在Director Server上，同时在Director Server上虚拟出一个IP地址，用户必须通过这个虚拟的IP地址访问服务。这个虚拟IP一般称为LVS的VIP，即Virtual IP。访问的请求首先经过VIP到达负载调度器，然后由负载调度器从Real Server列表中选取一个服务节点响应用户的请求。

  当用户的请求到达负载调度器后，调度器如何将请求发送到提供服务的Real Server节点，而Real Server节点如何返回数据给用户，是IPVS实现的重点技术，IPVS实现负载均衡机制有三种，分别是NAT、TUN和DR。
  
# 三种转发机制
VS/NAT： 即（Virtual Server via Network Address Translation） 
   网络地址翻译技术实现虚拟服务器（源地址目标地址转换）
   1. 当用户请求到达调度器时，调度器将请求报文的目标地址（即虚拟IP地址）改写成选定的Real Server地址
   2，同时报文的目标端口也改成选定的Real Server的相应端口，最后将报文请求发送到选定的Real Server
   3，在服务器端得到数据后，Real Server返回数据给用户时，需要再次经过负载调度器将报文的源地址和源端口改成虚拟IP地址和相应端口，然后把数据发送给用户，完成整个负载调度过程。
   4. 在NAT方式下，用户请求和响应报文都必须经过Director Server地址重写，当用户请求越来越多时，调度器的处理能力将称为瓶颈


VS/TUN ：即（Virtual Server via IP Tunneling）l 
   IP隧道技术实现虚拟服务器（多封装一个IP首部）
   1，VS/TUN方式中，调度器采用IP隧道技术将用户请求转发到某个Real Server
   2. 而这个Real Server将直接响应用户的请求，不再经过前端调度器
   3. 此外，对Real Server的地域位置没有要求，可以和Director Server位于同一个网段，也可以是独立的一个网络。因此，在TUN方式中，调度器将只处理用户的报文请求，集群系统的吞吐量大大提高。
   5. 如果跨区域需要公网IP地址
   

VS/DR： 即（Virtual Server via Direct Routing） 
   直接路由技术实现虚拟服务器（MAC转发）
   1. VS/DR通过改写请求报文的MAC地址，将请求发送到Real Server
   2， Real Server将响应直接返回给客户，免去了VS/TUN中的IP隧道开销。
   3. 这种方式是三种负载调度机制中性能最高最好的，但是必须要求Director Server与Real Server都有一块网卡连在同一物理网段上。 
   
   
```

### **NAT模式**

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\NAT模式.png)

```shell
1. 客户端发起请求到directory（lvs）的虚拟ip

2. directory（lvs）把客户请的目标地址改写为其中一个real server的，源地址改成不变。

3. realserver接受请求，并返回给directory（lvs）响应

4. directory（lvs）接受到响应，修改目标地址为不变，源地址改成自己的。

5. 客户端接受directory（lvs）的响应
```

### **DR模式**

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\DR模式.png)

```shell
1. 客户端发起请求到directory（lvs）的虚拟ip

2.directory（lvs）把客户发送的包，修改源mac地址为vip的，目的mac地址为realserver的，然后发送给realserver

3. realserver接受请求,并处理 然后把结果通过vip直接返回给客户端。

4. 客户端接受real server的响应。 

# 注意
a. directory（lvs）和realserver 使用相同的vip
b. directory（lvs）和realserver必须在同一个网络，因为load balancer需要知道realserver的mac地址。
```

### **TUN模式**

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\tun模式.png)

```shell
1. 客户端发起请求到directory（lvs）的虚拟ip

2. directory（lvs）把客户的请求包包裹，然后转发给其中的一个real server。

3. real server接受请求，解包。得到客户端发来的原始包。

4. real server处理，把结果通过vip直接返回给客户端。

5. 客户端接受real server的响应。 

注意：

a. directory（lvs）和realserver 直接通过ip tunnel技术重新封装、解包

b. directory（lvs）和 realserver 使用相同的vip

c. directory（lvs）和realserver可以不再同一个网络
```

## 模式优缺点:

![image-20240313101750060](C:\Users\THINKPAD\Desktop\keepalived\lvs\模式性能对比.png)

```shell
# 模式介绍
NAT模式: 基于NAT模式工作
  优点：
  	1. NAT 的优点是服务器可以运行任何支持TCP/IP的操作系统，它只需要一个IP地址配置在LVS主机上，服务器组可以用私有的IP地址。
  	2, 支持源地址目标地址转换
  缺点:
    1. 它的扩充能力有限，当服务器结点数目升到20时，LVS主机本身有可能成为系统的新瓶颈，
    2  在VS/NAT中请求和响应封包都需要通过负载平衡LVS主机。
       
DR模式:  基于MAC地址转换工作
  优点:
  	1. 响应流量不经过LVS节点 rs直接响应给client
  	2. 扩展性高
  	3. 没有IP封装消耗
  缺点:
    1. rs 要求于 lvs在同一个物理网络
    2. 不支持源地址目的地址转换


TUN模式: 基于ipip 多封装模式工作
   优点:
   	 1. 可以跨路由方式组件集群
   	 2. rs 响应流量直接响应client
   缺点:
   	 1. 依赖公网IP或者专用隧道
```

## lvs 调度算法:

```shell
# 常用算法
rr(轮询)： 静态算法
	1. 连接请求被分配到各个rs节点
	2. 无需记录连接状态
	3. 当节点性能不一致时不建议使用
	4. 流量大时可能会出现不一致情况
	
sh(源地址hash)： 静态算法
	1. 根据用户ip做绑定
	2. 保证整个系统的唯一出入口

dh(目的地址hash): 静态算法
   1. 根据请求的目的地址进行hash
   
lc(最少连接)：动态算法
	1. 连接会调度到rs连接数最少的节点
	lc：256*A+I=当前连接数
	
wlc(基于权重设置的最少连接)
	计算方式:
		W = 权重
		A = 活动连接
		I = 非活动连接
		W * A + I = 当前连接数
		
lblc（局部性的最少链接调度）
	1. 适用于cache环境
	2. lvs会根据请求源ip做调度，找到一台最近使用的rs节点
	3. 如果节点down机或者处于一般的连接负载，lvs将使用最少连接方式调度
lblcr(带复制的基于局部性最少链接调度)
	1. 适用于cache环境
	2. 于lblc不同点是 lblcr 维护了一组映射关系；而lblc只是维护了一个目标IP地址到一台服务器的映射
	3. 在cache环境中如果一个热门访问地址被频繁访问，那么lblc会根据负载情况调度，这样会有一个问题就是只映射一台始终会有负载过高的情况，lblcr 就是弥补了这个缺点，它会将热门站点映射到一组节点之上，，当该“热门”站点的请求负载增加时，会增加集合里的Cache服务器，来处理不断增长的负载；当该“热门”站点的请求负载降低时，会减少集合里的Cache服务器数目。
```

## lvs命令:

```shell
# 安装 ipvsadm
  ipvsadm是用户空间的一个工具，主要是用于配置和管理ipvs内核模块，ipvs是实现调度的核心模块
$ yum install ipvsadm 

# 获取帮助
$ ipvsadm --help


# 参数解析
-A --add-service 	添加虚拟服务
-E --edit-servie	修改虚拟服务
-D --delete-service 删除虚拟服务
-C --clear			清空lvs配置
-R --restore		在标准输入配置lvs规则，退出配置将保存到lvs规则
-S --save			保存规则
-t	--tcp-service	添加TCP协议虚拟服务
-u	--udp-service	添加UDP协议虚拟服务


rs相关

-a --add-server		向虚拟服务添加一台调度设备
-e --edit-server	修改调度设备配置
-d --delete-server	删除rs节点配置
-l -L--list			打印出lvs配置规则
-s	--scheduler		配置负载均衡规则

-g	--gatewaying	DR模式
-i	--ipip			TUN模式
-m	--masquerading	NAT模式
-w	--weight		rs权重配置
-c	--connection	rs允许连接最大数目
--timeout	
--rate				每秒发送到后端rs的速率
```

### lvs配置规则保存:

```shell
# 备份规则方式一
$ ipvsadm -S  >> ipvs.save

# 备份规则方式二
$ ipvsadm-save >> ipvs.save 



# 恢复规则方式一
$ ipvsadm-save -R < ipvs.save

# 恢复规则方式二
$ ipvsadm-restore < ipvs.save
```

## lvs使用:

### NAT模式:

![d](C:\Users\THINKPAD\Desktop\keepalived\lvs\08e43279d028397ebb5c68730a0cbe31.png)

```shell
# 描述
  nat模式下 rs网关要指向 directory节点 VIP
  1. rs 节点配置web服务
  2. rs 节点添加网关配置
  3. directory server 新增调度规则
  
 
# rs 节点配置
$ yum install httpd -t 
$ systemctl enabled --now htpp
$ ip route show // 网关指向VIP

# directory server 配置
$ yum install ipvsadm -y
$ echo 1 > /proc/sys/net/ipv4/ip_forward
$ ipvsadm  -C
$ ipvsadm  -A  -t 192.168.1.75:81 -s rr
$ ipvsadm -a -t 192.168.1.75:81  -r 192.168.1.100:8080 -m
$ ipvsadm -a -t 192.168.1.75:81  -r 192.168.1.76:8080 -m

# 验证
curl 192.168.1.75:80

```

**抓包分析**

192.168.255.102发送请求报文192.168.1.75的报文

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\lvs14102.png)

nat转换，把目标地址转换为realserver的地址

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\lvs14132.png)

realserver响应报文，返回给102,通过网关的

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\lvs14166.png)

网关进行转换 把源地址改成网关地址

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\lvs14187.png)

### DR模式:

```shell
# rs 节点执行脚本
#!/bin/bash
### BEGIN INIT INFO
# Provides:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start realserver
# Description:       Start realserver
### END INIT INFO

# change the VIP to proper value
VIP=192.168.1.240 

case "$1" in
    start)
    echo "Start REAL Server"
    /sbin/ifconfig lo:0 $VIP broadcast $VIP netmask 255.255.255.255 up
    echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore
    echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce
    echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce

    ;;

    stop)

    /sbin/ifconfig lo:0 down
    echo "Stop REAL Server"
    echo "0" >/proc/sys/net/ipv4/conf/lo/arp_ignore
    echo "0" >/proc/sys/net/ipv4/conf/lo/arp_announce
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_announce
    ;;

    restart)
    $0 stop
    $0 start
    ;;

    *)

    echo "Usage: $0 {start|stop}"
    exit 1

    ;;
esac

exit 0

# directory server 配置
$ ipvsadm -C
$ ipvsadm  -A  -t 192.168.1.240:8080 -s rr
$ ipvsadm -a -t 192.168.1.240:8080   -r 192.168.1.76:8080 -g
$ ipvsadm -a -t 192.168.1.240:8080   -r 192.168.1.100:8080 -g

$ ifconfig eth0:0 192.168.1.240  netmask 255.255.255.0  broadcast 192.168.1.255
```

**抓包分析**

流量到达directory server:

![image-20240313132115655](C:\Users\THINKPAD\Desktop\keepalived\lvs\image-20240313132115655.png)

此时directory server修改目的mac（rs某节点）

![image-20240313132341635](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240313132341635.png)

rs在接受到数据后拆包发现目的IP为本机VIP 走一圈lo网卡 处理完数据后直接返回client

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\lvs16539.png)

### TUN模式:

```shell
# 几台机器必须使用相同的vip和端口，对源请求再次封装，转发到实际的服务器上，服务器直接返回给客户端。

# directory server 配置
$ ipvsadm -C
$ ipvsadm  -A  -t 192.168.1.240:8080 -s rr
$ ipvsadm -a -t 192.168.1.240:8080   -r 192.168.1.76:8080 -i
$ ipvsadm -a -t 192.168.1.240:8080   -r 192.168.1.100:8080 -i

$ ifconfig tunl0 192.168.1.240  netmask 255.255.255.0  broadcast 192.168.1.255

# rs 节点配置
$ ifconfig tunl0 192.168.1.240  netmask 255.255.255.0  broadcast 192.168.1.255
 
# 防止发送和响应本机虚拟ip的arp

$ echo "1" > /proc/sys/net/ipv4/conf/all/arp_ignore
$ echo "1" > /proc/sys/net/ipv4/conf/lo/arp_ignore
$ echo "2" > /proc/sys/net/ipv4/conf/lo/arp_announce
$ echo "2" > /proc/sys/net/ipv4/conf/all/arp_announce
```

**抓包分析**

负载均衡器把163的请求报文，转到realserver上可以看到多封装了一层ip首部

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\lvs15110.png)

客户机请求报文和接受报文的情况

![img](C:\Users\THINKPAD\Desktop\keepalived\lvs\lvs15148.png)

# Keepalived

## 集群类型:

```shell
LB：Load Balance 负载均衡
	LVS/HAProxy/nginx（http/upstream, stream/upstream）
HA：High Availability 高可用集群
	数据库、Zookeeper、Redis
 	SPoF: Single Point of Failure，解决单点故障
HPC：High Performance Computing 高性能集群 
	https://www.top500.org
```

##  系统可用性:

```shell
SLA：Service-Level Agreement  服务等级协议（提供服务的企业与客户之间就服务的品质、水准、性
能等方面所达成的双方共同认可的协议或契约）

A = MTBF  / (MTBF+MTTR）
# 一个月内保持在99% 
# 小数点后面的数字越多那么系统的可用性越高
(60 * 24 * 30) * (1-0.99) = 7.2 小时

指标 ：99.9%, 99.99%, 99.999%,99.9999%
```

## 实现高可用:

```shell
提升系统高用性的解决方案：降低MTTR- Mean Time To Repair(平均故障时间)

解决方案：建立冗余机制

active/passive 主/备
active/active 双主 
active --> HEARTBEAT --> passive 
active <--> HEARTBEAT <--> active
```

## Keepalived简介:

```shell
keepalived 内置 vrrp程序 协议的软件实现，原生设计目的为了高可用 ipvs服务

官网：http://keepalived.org/

功能：
	1 基于vrrp协议完成地址流动
	2 为vip地址所在的节点生成ipvs规则(在配置文件中预先定义)
	3 为ipvs集群的各RS做健康状态检测
	4 基于脚本调用接口完成脚本中定义的功能，进而影响集群事务，以此支持nginx、haproxy等服务
```

### VRRP协议:

*局域网缺省网关示意图*

![局域网缺省网关示意图](C:\Users\THINKPAD\Desktop\keepalived\截图\download)

*VRRP备份组示意图*

![VRRP备份组示意图](C:\Users\THINKPAD\Desktop\keepalived\截图\vrrp架构图)

```shell
# 为什么需要VRRP
问题：
  1. 随着网络的快速普及和相关应用的日益深入，各种增值业务（如IPTV、视频会议等）已经开始广泛部署，基础网络的可靠性日益成为用户关注的焦点，能够保证网络传输不中断对于终端用户非常重要。
  2. 现网中的主机使用默认网关与外部网络联系时，如果Gateway出现故障，与其相连的主机将与外界失去联系，导致业务中断。
  
  VRRP的出现很好地解决了这个问题。VRRP将多台设备组成一个虚拟设备，通过配置虚拟设备的IP地址为缺省网关，实现缺省网关的备份。当网关设备发生故障时，VRRP机制能够选举新的网关设备承担数据流量，从而保障网络的可靠通信。如下图所示，当Master设备故障时，发往缺省网关的流量将由Backup设备进行转发。
```

### VRRP的工作原理:

*VRRP协议状态*

![image-20240306150134381](C:\Users\THINKPAD\Desktop\keepalived\截图\vrrp三种工作状态.png)

```shell
# VRRP的三种状态
  VRRP协议中定义了三种状态机：
  	初始状态（Initialize）
  	活动状态（Master）
  	备份状态（Backup）
  只有处于Master状态的设备才可以转发那些发送到虚拟IP地址的报文
```

### VRRP选举机制:

*Master设备选举过程*

![Master设备选举过程](C:\Users\THINKPAD\Desktop\keepalived\截图\master选举流程图)

```shell
# vrrp中术语
  虚拟路由: 0-255之间任意整数代表一个路由组，一般多台设备组成
  优先级:	选举过程中会根据优先级大小进行比较，最终来选举出master节点

# 选举方式
 由几台路由器组成的虚拟路由器又称为VRRP备份组。一个VRRP备份组在逻辑上为一台路由器。VRRP备份组建立后，各设备会根据所配置的优先级来选举Master设备
```

### VRRP工作原理:

*VRRP工作原理*

![VRRP工作原理](C:\Users\THINKPAD\Desktop\keepalived\截图\vrrp工作原理)

```shell
当Master设备出现故障时，路由器B和路由器C会选举出新的Master设备。新的Master设备开始响应对虚拟IP地址的ARP响应，并定期发送VRRP通告报文。

#VRRP的详细工作过程如下：
1. VRRP备份组中的设备根据优先级选举出Master。Master设备通过发送免费ARP报文，将虚拟MAC地址通知给与它连接的设备或者主机，从而承担报文转发任务。

2. Master设备周期性向备份组内所有Backup设备发送VRRP通告报文，通告其配置信息（优先级等）和工作状况。

3. 如果Master设备出现故障，VRRP备份组中的Backup设备将根据优先级重新选举新的Master。

4. VRRP备份组状态切换时，Master设备由一台设备切换为另外一台设备，新的Master设备会立即发送携带虚拟路由器的虚拟MAC地址和虚拟IP地址信息的免费ARP报文，刷新与它连接的设备或者主机的MAC表项，从而把用户流量引到新的Master设备上来，整个过程对用户完全透明。

5. 原Master设备故障恢复时，若该设备为IP地址拥有者（优先级为255），将直接切换至Master状态。若该设备优先级小于255，将首先切换至Backup状态，且其优先级恢复为故障前配置的优先级。
Backup设备的优先级高于Master设备时，由Backup设备的工作方式（抢占方式和非抢占方式）决定是否重新选举Master。
```

## keepalived架构:

*keepalived内部进程架构图*

![img](C:\Users\THINKPAD\Desktop\keepalived\截图\keepalived内部架构图.gif)

```shell

vrrp stack：vrrp 服务的实现 VIP消息通告

checkers：监测real server用来做健康状态检测

system call：实现 vrrp 协议状态转换时调用脚本的功能

SMTP：邮件组件

IPVS wrapper：生成IPVS规则

Netlink Reflector：网络接口

WatchDog：监控进程

控制组件：提供keepalived.conf 的解析器，完成Keepalived配置

IO复用器：针对网络目的而优化的自己的线程抽象

内存管理组件：为某些通用的内存管理功能（例如分配，重新分配，发布等）提供访问权限
```

## keepalived安装:

```shell
# 二进制包下载位置
  https://keepalived.org/download.html
  
# Centos系统下载编译所需rpm包
  yum -y install  gcc curl openssl-devel libnl3-devel net-snmp devel
# 解压&编译
  tar -axvf keepalived-2.2.8.tar.gz -C /data 
  cd keepalived-2.2.8/
  ./configure --prefix=/usr/local/keepalived-2.2.8 --disable-fwmark
  make && make install
  
# 创建配置文件目录
  mkdir /etc/keepalived
  cp /data/keealived-2.2.8/keepalived/etc/keepalived/keepalived.conf  
/etc/keepalived
```

## Keepalived配置:

```shell
keepalived 配置文件分为三个区域：
	
	global_defs： 通常配置邮件告警通知配置
	vrrp_instance: 	定义vrrp虚拟路由配置例如 优先级、VIP、角色状态、虚拟路由ID等
	virtual_server： keepalived内置生产lvs规则功能底层也是调用netfile内核模块完成，通常配置lvs 中rs节点信息、调度算法、LVS工作方式、健康状态检测等
```

### 全局配置区域:

```shell
#/etc/keepalived/keepalived.conf 
global_defs {
  notification_email {
  root@localhost             
	#keepalived 发生故障切换时邮件发送的目标邮箱，可以按行区分写多个
  	root@wangxiaochun.com 
	29308620@qq.com 
  }
  #发邮件的地址
  notification_email_from keepalived@localhost  
  #邮件服务器地址
  smtp_server 127.0.0.1     
  #邮件服务器连接timeout
  smtp_connect_timeout 30   
  #每个keepalived主机唯一标识，建议使用当前主机名，但多节点重名不影响
  router_id ka1.example.com 
  #对所有通告报文都检查，会比较消耗性能，启用此配置后，如果收到的通告报文和上一个报文是同一个路由器，则跳过检查，默认值为全检查
  vrrp_skip_check_adv_addr 
  #严格遵守VRRP协议,启用此项后以下状况将无法启动服务:1.无VIP地址 2.配置了单播邻居 3.在VRRP版本2中有IPv6地址，开启动此项并且没有配置vrrp_iptables时会自动开启iptables防火墙规则，默认导致VIP无法访问,建议不加此项配置
  vrrp_strict 
  #gratuitous ARP messages 报文发送延迟，0表示不延迟
  vrrp_garp_interval 0 
  #unsolicited NA messages （不请自来）消息发送延迟
  vrrp_gna_interval 0  
  #指定组播IP地址范围：224.0.0.0到239.255.255.255,默认值：224.0.0.18 
  vrrp_mcast_group4 224.0.0.18
  #此项和vrrp_strict同时开启时，则不会添加防火墙规则,如果无配置vrrp_strict项,则无需启用此项配置
  vrrp_iptables        
}
```

### VRRP配置区域:

```shell
vrrp_instance inside_network {
  # 初始状态，MASTER | BACKUP
  # 一旦其他机器启动，将进行选举，具有最高优先级的机器将变为MASTER。
  # 所以这里的配置并不重要。
  state MASTER

  # 为 inside_network 配置网络接口, 由 vrrp 绑定
  interface eth0

  # 使用VRRP虚拟MAC。
  use_vmac [<VMAC_INTERFACE>]

  # 从基本接口（而不是VMAC接口）发送/恢复VRRP消息
  vmac_xmit_base

  native_ipv6         # 强制实例使用IPv6（混合IPv4和IPv6配置时）。

  # 忽略VRRP接口故障（默认未设置）
  dont_track_primary

  # 可选，监视
  # 如果任何一个下降，进入FAULT状态。
  track_interface {
    eth0
    eth1
    eth2 weight <-254..254>
    ...
  }

  # 向接口添加跟踪脚本（<SCRIPT_NAME>是vrrp_script条目的名称）
  track_script {
      <SCRIPT_NAME>
      <SCRIPT_NAME> weight <-254..254>
  }

  # 默认 vrrpd 绑定的 IP 是接口上的主 IP 。 （可选的）
  # 如果要隐藏 vrrpd 的位置，请将此 IP 当做 src_addr 用于组播或单播 vrrp 数据包。 （
  # 因为它是多播，vrrpd 将获得答复数据包，无论使用什么 src_addr ）。
  mcast_src_ip <IPADDR>
  unicast_src_ip <IPADDR>

  version <2 or 3>            # VRRP版本在接口上运行
                              # default是全局参数vrrp_version。

  # 不要通过 VRRP 组播组发送 VRRP adverts
  # 相反，它使用单播将 adverts 发送到以下IP地址列表。 在不支持多播的网络环境中使用VRRP FSM和功能可能很酷！
  # 指定的IP地址可以是IPv4和IPv6。
  unicast_peer {
    <IPADDR>
    ...
  }
  # 接口特定设置，与全局参数相同; 默认为全局参数
  garp_master_delay 10
  garp_master_repeat 1
  garp_lower_prio_delay 10
  garp_lower_prio_repeat 1
  garp_master_refresh 60
  garp_master_refresh_repeat 2
  garp_interval 100
  gna_interval 100

  lower_prio_no_advert [<BOOL>]

  # 从0到255的任意唯一编号，用于区分在同一NIC（和相同的套接字）上运行的vrrpd的多个实例。
  virtual_router_id 51

  # 用于选择MASTER，最高优先级的会被选举出来。
  # 超过50个以上的其它机器的设置，会被选为 MASTER
  priority 100

  # VRRP广告间隔（以秒为单位）（例如0.92）（使用默认值）
  advert_int 1

  # 注意：在2004年，RFC3768 从 VRRPv2 规范中删除了身份验证。
  # 此选项的使用不符合规定，可能会导致问题;
  # 所以尽可能避免使用，除非使用单播。
  authentication {     # 验证块
      # PASS||AH
      #   PASS - 简单密码（建议）
      #   AH - IPSEC（不推荐）
      auth_type PASS
      # 访问vrrpd的密码。
      # 应在所有机器上相同。
      # 只使用前八（8）个字符。
      auth_pass 1234
  }

  # 设置虚拟IP地址，所有的机器上应该都使用相同的配置
  virtual_ipaddress {
      <IPADDR>/<MASK> brd <IPADDR> dev <STRING> scope <SCOPE> label <LABEL>
      192.168.200.17/24 dev eth1
      192.168.200.18/24 dev eth2 label eth2:1
  }

  # 从可选的VRRP中排除VRRP IP。
  # 对于在同一接口上有大量（例如200）的IP的情况。 要减少广告中发送的数据包数量，我们可以从广告中排除大多数IP。

  # 为virtual_ipaddress添加或者删除。
  # 因为virtual_ipaddress中的所有地址必须是同一系列，所以如果我们希望能够添加IPv4和IPv6地址的混合，也可以使用，virtual_ipaddress_excluded 来进行配置。
  virtual_ipaddress_excluded {
   <IPADDR>/<MASK> brd <IPADDR> dev <STRING> scope <SCOPE>
   <IPADDR>/<MASK> brd <IPADDR> dev <STRING> scope <SCOPE>
      ...
  }


  # 设置接口上的promote_secondaries标志，以便在删除其中一个时，停止删除同一CIDR中的其他地址。例如，如果在接口上同时配置了10.1.1.2/24和10.1.1.3/24，一旦删除了一个，除非接口上设置了 promote_secondaries 标志，否则其他地址也将会被删除。
  prompte_secondaries

  # 当转换成 MASTER 时添加下面的routes，当转换成 BACKUP 时，会删除下面的routes 配置
  # 有关详细信息，请参阅static_routes
  virtual_routes {
      # src <IPADDR> [to] <IPADDR>/<MASK> via|gw <IPADDR> [or <IPADDR>] dev <STRING> scope <SCOPE> table <TABLE>
      src 192.168.100.1 to 192.168.109.0/24 via 192.168.200.254 dev eth1
      192.168.110.0/24 via 192.168.200.254 dev eth1
      192.168.111.0/24 dev eth2
      192.168.112.0/24 via 192.168.100.254
      192.168.113.0/24 via 192.168.200.254 or 192.168.100.254 dev eth1
      blackhole 192.168.114.0/24
      0.0.0.0/0 gw 192.168.0.1 table 100  # To set a default gateway into table 100.
  }

  # 当转换成 MASTER 时添加下面的 rules ，当转换成 BACKUP 时，会删除下面的 rules 配置
  # 有关详细信息，请参阅static_rules
  virtual_rules {
      from 192.168.2.0/24 table 1
      to 192.168.2.0/24 table 1
  }

  # VRRPv3有一个 接受模式，以允许虚拟路由器在没有地址所有者时接收发往VIP的数据包。 这是默认设置，除非设置了strict模式。
  # 作为扩展，这也适用于VRRPv2（RFC 3768没有定义接受模式）。
  accept          # 接受数据包到非地址所有者
  no_accept       # 丢弃数据包到非地址所有者。

  # 当较高优先级机器联机时，VRRP通常抢占较低优先级机器。 “nopreempt”允许较低优先级机器维护主机角色，即使较高优先级机器恢复在线时也是如此。
  # 注意：要使其工作，此条目的初始状态必须为BACKUP。
  nopreempt
  preempt             # 用于向后兼容


   # 请参见全局vrrp_skip_check_adv_addr的描述，它设置默认值。 默认为vrrp_skip_check_adv_addr
   skip_check_adv_addr [on|off|true|false|yes|no]      # 如果没有指定，默认开启

   # 请参见全局vrrp_strict的描述
   # 如果未指定vrrp_strict，则它使用vrrp_strict的值
   # 如果指定了不带参数的strict_mode，则其默认为on
   strict_mode [on|off|true|false|yes|no]

   # 启动后的秒数或看到较低优先级主机直到抢占（如果未由“nopreempt”禁用）。
   # Range: 0 (default) to 1000
   # 注意：要使其工作，此条目的初始状态必须为BACKUP。
   preempt_delay 300    # 等待5分钟

   # 调试级别，尚未实现。
   debug <LEVEL>        # LEVEL是0到4范围内的数字

   # 通知脚本，警报如上
   notify_master <STRING>|<QUOTED-STRING> [username [groupname]]
   notify_backup <STRING>|<QUOTED-STRING> [username [groupname]]
   notify_fault <STRING>|<QUOTED-STRING> [username [groupname]]
   notify_stop <STRING>|<QUOTED-STRING> [username [groupname]]      # 在停止vrrp时执行
   notify <STRING>|<QUOTED-STRING> [username [groupname]]
   smtp_alert
}

# 用于SSL_GET检查的参数。
# 如果未指定任何参数，则将自动生成SSL上下文。
SSL {
   password <STRING>   # 密码
   ca <STRING>         # ca文件
   certificate <STRING>  # 证书文件
   key <STRING>        # 密钥文件
}          
```

### LVS虚拟服务区域:

#### Virtual Server Group(虚拟服务组):

```shell
  virtual server group（虚拟服务组），主要功能是可以将多个Virtual server 定义到一个组内管理，这种方式可以使配置更清晰简介，统一管理和维护。
  
 # 定义方式
 
 virtual_server_group my_vs_group {
 
 		lvs_sched rr
 		protocol TCP
 		virtual_server 133.133.1.99 80 {
 			delay_loop 6
 			lb_algo rr
 			lb_kind DR
 				real_server 133.133.1.10 80 {
 						weight 1 
 					
 				}
 				
 		 virtual_server 133.133.1.100 80 {
 			delay_loop 6
 			lb_algo rr
 			lb_kind DR
 				real_server 133.133.1.11 80 {
 						weight 1 			
 				}
 	
 		}
 
 }

```

#### Virtual Server 虚拟服务:

```shell
  virtaul server 定义lvs配置的

# 设置服务
virtual_server IP port |
virtual_server fwmark int |
virtual_server group string
{
# 延迟定时器用于服务轮询
delay_loop <INT>

# LVS调度器
lb_algo rr|wrr|lc|wlc|lblc|sh|dh

# 启用散列条目
hashed
# 启用 flag-1 调度器 (-b flag-1 in ipvsadm)
flag-1
# 启用 flag-2 调度器(-b flag-2 in ipvsadm)
flag-2
# 启用 flag-3 调度器 (-b flag-3 in ipvsadm)
flag-3
# 启用 sh-port 调度器 (-b sh-port in ipvsadm)
sh-port
# 启用 sh-fallback 调度器  (-b sh-fallback in ipvsadm)
sh-fallback

# 为UDP启用单分组调度（在ipvsadm中为-O）
ops
# LVS转发方法
lb_kind NAT|DR|TUN
# LVS持久超时，秒
persistence_timeout <INT>
# LVS粒度掩码（ipvsadm中的-M）
persistence_granularity <NETMASK>
# 仅实现TCP
protocol TCP
# 如果没有设置VS IP地址，则暂停healthchecker的活动
ha_suspend

# 用于HTTP_GET或SSL_GET的VirtualHost字符串
# 例如 virtualhost www.firewall.loc
virtualhost <STRING>

# 假定所有RS关闭,并且在启动时检查运行状况失败。
# 这有助于防止启动时的假的积极操作。 默认情况下禁用Alpha模式。
alpha

# 在守护程序关闭时，在适当的情况下，考虑降低仲裁和RS通知程序执行。
# 默认情况下禁用Omega模式。
omega

# Minimum total weight of all live servers in
# the pool necessary to operate VS with no
# quality regression. Defaults to 1.
quorum <INT>

# Tolerate this much weight units compared to the
# nominal quorum, when considering quorum gain
# or loss. A flap dampener. Defaults to 0.
hysteresis <INT>

# 获得 quorum 时启动的脚本。
quorum_up <STRING>|<QUOTED-STRING>

# 丢失quorum时启动的脚本。
quorum_down <STRING>|<QUOTED-STRING>

# 设置 realserver(s)

# 在所有 realserver 都关闭时生效
sorry_server <IPADDR> <PORT>
# 将 inhibit_on_failure 行为应用于前面的 sorry_server 指令
sorry_server_inhibit

# 每个realserver,一个条目
real_server <IPADDR> <PORT>
  {
      # 相对权重，默认：1
      weight <INT>
      # 健康检查器检测到故障时，将权重设置为0
      inhibit_on_failure

      # 当运行状况检查器将服务视为启动时启动的脚本。
      notify_up <STRING>|<QUOTED-STRING>
      # 当运行状况检查器将服务视为停机时启动的脚本。
      notify_down <STRING>|<QUOTED-STRING>

      # 选择一个健康检查
      # HTTP_GET|SSL_GET|TCP_CHECK|SMTP_CHECK|MISC_CHECK

      # HTTP和SSL健康检查程序
      HTTP_GET|SSL_GET
      {
          # 一个url测试
          # 可以有多个条目
          url {
            # 例如 path / , or path /mrtg2/
            path <STRING>
            # healthcheck需要status_code或status_code和digest
            # 摘要用genhash计算
            # 例如 digest 9b3a0c85a887a256d6939da88aabd8cd
            digest <STRING>
            # HTTP标头中返回的状态代码
            # 例如 status_code 200
            status_code <INT>
          }
          # 获取重试次数
          nb_get_retry <INT>
          # 延迟后重试
          delay_before_retry <INT>

          # ======== 通用连接选项
          # 要连接的可选IP地址。
          # 默认值为真实服务器的IP
          connect_ip <IP ADDRESS>
          # 可选，端口，如果没有连接
          # 默认值为真实服务器的端口
          connect_port <PORT>
          # 用于发起连接的可选接口
          bindto <IP ADDRESS>
          # 用于发起连接的可选源端口
          bind_port <PORT>
          # 可选，连接超时（秒）。
          # 默认值为5秒
          connect_timeout <INTEGER>
          # 可选，用于标记所有传出检查程序包的fwmark
          fwmark <INTEGER>

          # 可选的，随机延迟最大N秒后开始初始检查。
          # 用于将多个同时检查分散到同一个RS。 默认情况下启用，最大值为delay_loop。 指定 0 为禁用
          warmup <INT>
      } # HTTP_GET|SSL_GET

      # TCP健康检查器（绑定到IP端口）
      TCP_CHECK
      {
          # ======== 通用连接选项
          # 可选，要连接的IP地址。
          # 默认值为真实服务器的IP
          connect_ip <IP ADDRESS>
          # 可选，连接端口
          # 默认值为真实服务器的端口
          connect_port <PORT>
          # 可选，发起连接使用的接口
          bindto <IP ADDRESS>
          # 可选，发起连接源端口
          bind_port <PORT>
          # 可选，连接超时（以秒为单位）。
          # 默认值为5秒
          connect_timeout <INTEGER>
          # 可选， 用于标记所有传出检查程序包的fwmark
          fwmark <INTEGER>

          # 可选， 随机延迟最大N秒后开始初始检查。
          # 用于将多个同时检查分散到同一个RS。 默认情况下启用，最大值为delay_loop。 指定 0 为禁用
          warmup <INT>
      } #TCP_CHECK

      # SMTP健康检查器
      SMTP_CHECK
      {
          # 可选，主机接口检查。
          # 如果没有主机指令，则只检查真实服务器的IP地址。
          host {
            # ======== 通用连接选项
            # 可选，要连接的IP地址。
            # 默认值为真实服务器的IP
            connect_ip <IP ADDRESS>
            # 可选，连接端口
            # 默认值为25
            connect_port <PORT>
            # 可选，发起连接使用的接口
            bindto <IP ADDRESS>
            # 可选，发起连接源端口
            bind_port <PORT>
            # 可选，每个主机连接超时。
            # Default is outer-scope connect_timeout
            connect_timeout <INTEGER>
            # 可选， 用于标记所有传出检查程序包的fwmark
            fwmark <INTEGER>
         }
         # 连接超时时间
         connect_timeout <INTEGER>
         # 重试失败检查的次数
         retry <INTEGER>
         # 重试前延迟秒
         delay_before_retry <INTEGER>
         # 用于smtp HELO请求的可选字符串
         helo_name <STRING>|<QUOTED-STRING>

         # 可选， 随机延迟最大N秒后开始初始检查。
         # 用于将多个同时检查分散到同一个RS。 默认情况下启用，最大值为delay_loop。 指定 0 为禁用
         warmup <INT>
      } #SMTP_CHECK

      # 运行外部程序，进行MISC健康检查
      MISC_CHECK
      {
          # 外部系统脚本或程序
          misc_path <STRING>|<QUOTED-STRING>
          # 脚本执行超时
          misc_timeout <INT>

          # 可选， 随机延迟最大N秒后开始初始检查。
          # 用于将多个同时检查分散到同一个RS。 默认情况下启用，最大值为delay_loop。 指定 0 为禁用
          warmup <INT>

          # 如果设置，将会根据  healthchecker 退出状态码动态调整权重如下：
          #   exit status 0: svc检查成功，权重不变。
          #   exit status 1: svc检查失败.
          #   exit status 2-255: svc检查成功，权重更改为小于退出状态2的值。
          #   (示例：退出状态为 255 会将权重设置为 253 )
          misc_dynamic
          # 指定脚本应在其下运行的用户名/组名。 如果未指定GROUPNAME，则使用用户的组
          user USERNAME [GROUPNAME]
      }
  } # realserver 定义
} # virtual service

```



```shell
# 定义lvs 虚拟服务
# 等价于 ipvsadm -A -t 192.168.200.100:443 -s rr
virtual_server 192.168.200.100 443 {
    # 在给后段rs做健康状态检测时，俩次检查间隔时间
    delay_loop 6
    # lvs schedule 模式
    # 支持模式: rr|wrr|lc|wlc|lblc|sh|mh|dh|fo|ovf|lblcr|sed|nq|twos
    lb_algo rr
    # lvs 架构使用的方案
    # 支持: NAT|DR|TUN
    lb_kind NAT
    # 持久链接超时时间
    persistence_timeout 50
    # 4层协议
    # TCP|UDP|SCTP
    protocol TCP
    # rs 配置
    # ipvsadm -a -t 192.168.200.100:443 -r 192.168.201.100:443 -m -w 1 
    real_server 192.168.201.100 443 {
        # 权重配置
        weight 1
        # SSL健康状态检查
        SSL_GET {
            url {
              path /
              digest ff20ad2481f97b1754ef3e12ecd3a9cc
            }
            url {
              path /mrtg/
              digest 9b3a0c85a887a256d6939da88aabd8cd
            }
            connect_timeout 3
            retry 3
            delay_before_retry 3
        }
    }
}

virtual_server 10.10.10.2 1358 {
    delay_loop 6
    lb_algo rr
    lb_kind NAT
    persistence_timeout 50
    protocol TCP
    # 当10.10.10.2 虚拟服务后端rs 都不可用时调用sorry_server
    sorry_server 192.168.200.200 1358

    real_server 192.168.200.2 1358 {
        weight 1
        # http 协议状态检测
        HTTP_GET {
            url {
              path /testurl/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            url {
              path /testurl2/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            url {
              path /testurl3/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            connect_timeout 3
            retry 3
            delay_before_retry 3
        }
    }

    real_server 192.168.200.3 1358 {
        weight 1
        HTTP_GET {
            url {
              path /testurl/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334c
            }
            url {
              path /testurl2/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334c
            }
            connect_timeout 3
            retry 3
            delay_before_retry 3
        }
    }
}

virtual_server 10.10.10.3 1358 {
    delay_loop 3
    lb_algo rr
    lb_kind NAT
    persistence_timeout 50
    protocol TCP

    real_server 192.168.200.4 1358 {
        weight 1
        HTTP_GET {
            url {
              path /testurl/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            url {
              path /testurl2/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            url {
              path /testurl3/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            connect_timeout 3
            retry 3
            delay_before_retry 3
        }
    }

    real_server 192.168.200.5 1358 {
        weight 1
        HTTP_GET {
            url {
              path /testurl/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            url {
              path /testurl2/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            url {
              path /testurl3/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            connect_timeout 3
            retry 3
            delay_before_retry 3
        }
    }
}

```



## Keepalived功能配置:

### VRRP Script:

```shell
  vrrp script 主要功能是执行一个指定脚本，根据脚本返回的状态码 来对当前vrrp 优先级做调整，比如脚本执行失败将优先级 -50 那么 原本 100的有优先级只剩50，这将会影响到vrrp state运行模式。
 
 # 配置格式
 
 vrrp_script <SCRIPT_NAME> {
  script <STRING>|<QUOTED-STRING> # 脚本的路径执行
  interval <INTEGER>  # 脚本调用之间的间隔，默认1秒
  timeout <INTEGER>   # 脚本运行超时时间
  weight <INTEGER:-254..254>  # 按此权重调整优先级，默认为2
  rise <INTEGER>              # 转换为OK状态，所需的成功数量
  fall <INTEGER>              # 转换为KO状态，所需的成功数量
  user USERNAME [GROUPNAME]   # 运行脚本的 用户/组名 （组默认为用户组）
  init_fail                   # 假设脚本最初处于失败状态
}


```

### VRRP 同步组:

```shell
  vrrp_sync_group  是用来实现多个VIP同时来做故障转移的，组内可以定义多个VIP这将被当做一个整体来看做，只要组内有一个VIP服务发生故障进行了切换动作；那么组内其他成员将一同进行迁移。
  
# 定义方式
vrrp_sync_group VG_1 {
   group {
     inside_network   # vrrp_instance的名称（见下文）
     outside_network  # One for each movable IP
     ...
   }

   # 通知脚本和警报（可选）
   #
   ＃filenames的脚本在转换时运行，可以不加引号（如果只是文件名）或加引号（如果它有参数）用户名和组名指定脚本应该运行的用户和组。
   ＃如果指定了username，则组默认为用户的组。
   ＃如果未指定username，则它们默认为全局 script_user 和 script_group 到 MASTER 转换

   notify_master /path/to_master.sh [username [groupname]]
   # 转换成 BACKUP 状态
   notify_backup /path/to_backup.sh [username [groupname]]
   # 转换成 FAULT
   notify_fault "/path/fault.sh VG_1" [username [groupname]]

   # for ANY state transition.
   # "notify" script is called AFTER the
   # notify_* script(s) and is executed
   # with 3 arguments provided by Keepalived
   # (so don’t include parameters in the notify line).
   # arguments

   ＃ 对于任何状态的转换。
   ＃ “notify”脚本在 notify_* 脚本之后调用，并使用 Keepalived 提供的3个参数执行（不包括通知行中的参数）。
   ＃ 参数：
   #    $1 = "GROUP"|"INSTANCE"
   #    $2 = 组或实例的名称
   #    $3 = 转型目标状态 ("MASTER"|"BACKUP"|"FAULT")
   notify /path/notify.sh [username [groupname]]

   # 在状态转换期间使用global_defs中的地址发送电子邮件通知。
   smtp_alert

   global_tracking     # 所有VRRP共享相同的跟踪配置
}

```



### 告警邮件通知功能:

#### 本地mail配置:

```shell
Centos 可以利用mailx 来实现邮件发送功能，需要配置好smtp

# 安装mailx
$ yum install maix -y

# 配置mailx
# 最低端新增即可
$ vim /etc/mail.rc
    set from=17600169910@163.com		// 邮件接收邮箱
    set smtp=smtp.163.com				// 邮箱的smtp服务器地址
    set smtp-auth-user=17600169910@163.com	//  认证邮箱地址写接收地址
    set smtp-auth-password=ZBHLBCZTDJWCQBKT	// 163邮箱设置里开启smtp获取
    set smtp-auth=login					// 启用smtp认证功能
    
# 测试邮件接收是否正常
echo “Test Send Mail” | mail -s ‘Test Send Info..’ 17600169910@163.com
```

#### keepalived  消息通知机制:

*邮件通知*

![image-20240309150432407](C:\Users\THINKPAD\Desktop\keepalived\截图\邮件通知截图.png)

```shell
  keepalived的状态变化时，可以自动触发脚本的执行，比如：发邮件通知用户默认以用户keepalived_script身份执行脚本，如果此用户不存在，以root执行脚本可以用下面指令指定脚本执行用户的身份.

	global_defs {
	 ......
 	 script_user <USER>
 	 ......notify_master <STRING>|<QUOTED-STRING>
 	}
 	
 脚本通知类型
   # 当节点角色切换到Master
   notify_master <STRING>|<QUOTED-STRING>
   # 当节点切换到Slave
   notify_backup <STRING>|<QUOTED-STRING>
   # 当前节点转为“失败”状态时触发的脚本 
   notify_fault <STRING>|<QUOTED-STRING>
   # 通用格式的通知触发机制，一个脚本可完成以上三种状态的转换时的通知
   notify <STRING>|<QUOTED-STRING>
   # 当停止VRRP时触发的脚本
   notify_stop <STRING>|<QUOTED-STRING>
 
 脚本通知配置区域:
    vrrp_instance VI_1 {
    	....
    	....
    	notify_master "/etc/keepalived/notify.sh master"
 		notify_backup "/etc/keepalived/notify.sh backup"
 		notify_fault "/etc/keepalived/notify.sh fault"  
    }

 创建通知脚本:
 $ vim /etc/keepalived/alert.sh
    #!/bin/bash
    #
    contact='17600169910@163.com'
    notify() {
      mailsubject="$(hostname) to be $1, vip floating"
      mailbody="$(date +'%F %T'): vrrp transition, $(hostname) vrrp_instance: $2  changed to be $1"
      echo "$mailbody" | mail -s "$mailsubject" $contact
    }
    case $1 in
            master)
                    notify master $2
            ;;
            backup)
                    notify backup $2
     ;;
            fault)
                    notify fault $2
            ;;
            *)
                    echo "Usage: $(basename $0) {master|backup|fault}"
                    exit 1
            ;;
    esac

# 配置邮件通知
$ vim /etc/keepalived/keepalived.conf
  ! Configuration File for keepalived

    global_defs {
       notification_email {
         17600169910@163.com
       }
       notification_email_from 17600169910@163.com 
       smtp_server smtp.163.com 
       smtp_connect_timeout 30
       router_id keepalived01
       vrrp_skip_check_adv_addr
       vrrp_strict
       vrrp_garp_interval 0
       vrrp_gna_interval 0
    }

    vrrp_instance VI_1 {
        state MASTER 
        interface eth0
        virtual_router_id 66
        priority 100
        advert_int 1
        authentication {
            auth_type PASS
            auth_pass 123456
        }
        unicast_src_ip 133.133.1.10
        unicast_peer {
        133.133.1.11	
        }
        virtual_ipaddress {
        133.133.1.99/32	dev eth0 label eth0:0
        }
        notify_master "/etc/keepalived/alert.sh master VI_1:vip-133.133.1.99"
        notify_slave "/etc/keepalived/alert.sh slave VI_1:vip-133.133.1.99"
    }
    vrrp_instance VI_2 {
        state BACKUP
        interface eth0
        virtual_router_id 77
        priority 80
        advert_int 1
        authentication {
            auth_type PASS
            auth_pass 1qaz@WSX
        }
        unicast_src_ip 133.133.1.10
        unicast_peer {
            133.133.1.11
        }
        virtual_ipaddress {
            133.133.1.88/32 dev eth0 label eth0:1
        }
        notify_master "/etc/keepalived/alert.sh master VI_1:vip-133.133.1.88"
        notify_slave "/etc/keepalived/alert.sh slave VI_1:vip-133.133.1.88"
    }
```

### keepalived启用日志功能:

```shell
# 修改配置
$ vim /usr/local/keepalived/etc/sysconfig/keepalived
  KEEPALIVED_OPTIONS="-D -S 6"
  
# 验证是否开启
tail -f /var/log/keepalived.log
```

## keepalived常用使用架构:

### Master/Slave抢占模式:

*单播模式抓包*

![image-20240309140734942](C:\Users\THINKPAD\Desktop\keepalived\截图\单播模式抓包.png)

```shell
# 编译安装keepalived
# 此模式抢占模式
# 配置文件修改Master
! Configuration File for keepalived

global_defs {
   notification_email {
     17600169910@163.com
   }
   notification_email_from 17600169910@163.com
   smtp_server smtp.163.com
   smtp_connect_timeout 30
   router_id keepalived01
   vrrp_skip_check_adv_addr
   vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 66
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
   # unicast_src_ip 133.133.1.10
   # unicast_peer {
   #     133.133.1.11
   # }
    virtual_ipaddress {
        133.133.1.99/32 dev eth0 label eth0:0
    }
}

# 配置文件slave
! Configuration File for keepalived

global_defs {
   notification_email {
     17600169910@163.com
   }
   notification_email_from 17600169910@163.com 
   smtp_server smtp.163.com 
   smtp_connect_timeout 30
   router_id keepalived02
   vrrp_skip_check_adv_addr
   vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
    state BACKUP 
    interface eth0
    virtual_router_id 66
    priority 90
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    # 单播模式
   # unicast_src_ip 133.133.1.11
   # unicast_peer {
   # 133.133.1.10	
   # }
    virtual_ipaddress {
	133.133.1.99/32	dev eth0 label eth0:0
    }
}

```

### Master/Slave非抢占模式:

```shell
# 抢占模式下会根据优先级来定位谁优先级大；那么他必须当作master节点
# 非抢占模式减少了来回切换vip；减少了网络延迟和丢数据包、网络抖动问题
# 非抢占模式下双方都使用BACKUP模式


关键配置:
	# 指定抢占延迟时间为#s，默认延迟300s
	preempt_delay 
    # 非抢占模式
	nopreempt
     

# 节点配置一
! Configuration File for keepalived

global_defs {
   notification_email {
     17600169910@163.com
   }
   notification_email_from 17600169910@163.com 
   smtp_server smtp.163.com 
   smtp_connect_timeout 30
   router_id keepalived01
   vrrp_skip_check_adv_addr
   vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
	# BACKUP角色
    state BACKUP
    # 不抢占模式
    nopreempt 
    interface eth0
    virtual_router_id 66
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    unicast_src_ip 133.133.1.10
    unicast_peer {
	133.133.1.11	
    }
    virtual_ipaddress {
	133.133.1.99/32	dev eth0 label eth0:0
    }
}

# 节点配置二
! Configuration File for keepalived

global_defs {
   notification_email {
     17600169910@163.com
   }
   notification_email_from 17600169910@163.com
   smtp_server smtp.163.com
   smtp_connect_timeout 30
   router_id keepalived02
   vrrp_skip_check_adv_addr
   vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
    state BACKUP
    nopreempt
    interface eth0
    virtual_router_id 66
    priority 90
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    unicast_src_ip 133.133.1.11
    # 目的IP可配置多个
    unicast_peer {
        133.133.1.10
    }
    virtual_ipaddress {
        133.133.1.99/32 dev eth0 label eth0:0
    }
}
```

### Master/Master抢占模式:

*双主模式下抓包*

![image-20240309142649236](C:\Users\THINKPAD\Desktop\keepalived\截图\双主模式抓包.png)

```shell
# Master/Slave 模式下当流量巨曾可能会出现单点问题出现
# Master/Master模式下每个节点均配置一个Master角色的VIP 流量请求可以通过LB代理
# 此模式下不建议使用非抢占模式双master让VIP分配到不同节点

# Mater
! Configuration File for keepalived

global_defs {
   notification_email {
     17600169910@163.com
   }
   notification_email_from 17600169910@163.com 
   smtp_server smtp.163.com 
   smtp_connect_timeout 30
   router_id keepalived01
   vrrp_skip_check_adv_addr
   vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
	# 节点一Master
    state MASTER 
    interface eth0
    virtual_router_id 66
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    unicast_src_ip 133.133.1.10
    unicast_peer {
	133.133.1.11	
    }
    virtual_ipaddress {
	133.133.1.99/32	dev eth0 label eth0:0
    }
}
vrrp_instance VI_2 {
    state BACKUP
    interface eth0
    virtual_router_id 77
    priority 80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1qaz@WSX
    }
    unicast_src_ip 133.133.1.10
    unicast_peer {
        133.133.1.11
    }
    virtual_ipaddress {
        133.133.1.88/32 dev eth0 label eth0:1
    }
}

# Master
! Configuration File for keepalived

global_defs {
   notification_email {
     17600169910@163.com
   }
   notification_email_from 17600169910@163.com 
   smtp_server smtp.163.com 
   smtp_connect_timeout 30
   router_id keepalived01
   vrrp_skip_check_adv_addr
   vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
    state BACKUP 
    interface eth0
    virtual_router_id 66
    priority 80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    unicast_src_ip 133.133.1.11
    unicast_peer {
	133.133.1.10	
    }
    virtual_ipaddress {
	133.133.1.99/32	dev eth0 label eth0:0
    }
}
vrrp_instance VI_2 {
    # 节点二Master
    state MASTER
    interface eth0
    virtual_router_id 77
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1qaz@WSX
    }
    unicast_src_ip 133.133.1.11
    unicast_peer {
        133.133.1.10
    }
    virtual_ipaddress {
        133.133.1.88/32 dev eth0 label eth0:1
    }
}
```

## keepalived 高可用lvs配置:

*keepalived架构图*

![image-20240309151829891](C:\Users\THINKPAD\Desktop\keepalived\截图\keepalived lvs.png)

```shell
  keepalived 最开始主要是为IPVS高可用的，所以keepalived 内置了调用natfiter的钩子，可以生成IPVS规则，并且支持健康检查算法。
  
  
# 定义lvs 虚拟服务
# 等价于 ipvsadm -A -t 192.168.200.100:443 -s rr
virtual_server 192.168.200.100 443 {
    # 在给后段rs做健康状态检测时，俩次检查间隔时间
    delay_loop 6
    # lvs schedule 模式
    # 支持模式: rr|wrr|lc|wlc|lblc|sh|mh|dh|fo|ovf|lblcr|sed|nq|twos
    lb_algo rr
    # lvs 架构使用的方案
    # 支持: NAT|DR|TUN
    lb_kind NAT
    # 持久链接超时时间
    persistence_timeout 50
    # 4层协议
    # TCP|UDP|SCTP
    protocol TCP
    # rs 配置
    # ipvsadm -a -t 192.168.200.100:443 -r 192.168.201.100:443 -m -w 1 
    real_server 192.168.201.100 443 {
        # 权重配置
        weight 1
        # SSL健康状态检查
        SSL_GET {
            url {
              path /
              digest ff20ad2481f97b1754ef3e12ecd3a9cc
            }
            url {
              path /mrtg/
              digest 9b3a0c85a887a256d6939da88aabd8cd
            }
            connect_timeout 3
            retry 3
            delay_before_retry 3
        }
    }
}

virtual_server 10.10.10.2 1358 {
    delay_loop 6
    lb_algo rr
    lb_kind NAT
    persistence_timeout 50
    protocol TCP
    # 当10.10.10.2 虚拟服务后端rs 都不可用时调用sorry_server
    sorry_server 192.168.200.200 1358

    real_server 192.168.200.2 1358 {
        weight 1
        # http 协议状态检测
        HTTP_GET {
            url {
              path /testurl/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            url {
              path /testurl2/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            url {
              path /testurl3/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334d
            }
            connect_timeout 3
            retry 3
            delay_before_retry 3
        }
    }

    real_server 192.168.200.3 1358 {
        weight 1
        HTTP_GET {
            url {
              path /testurl/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334c
            }
            url {
              path /testurl2/test.jsp
              digest 640205b7b0fc66c1ea91c463fac6334c
            }
            connect_timeout 3
            retry 3
            delay_before_retry 3
        }
    }
}

```

#### keepalived Lvs DR模式配置:

```shell
# keepalived 配置文件
! Configuration File for keepalived

global_defs {
   notification_email {
     17600169910@163.com
   }
   notification_email_from 17600169910@163.com 
   smtp_server smtp.163.com 
   smtp_connect_timeout 30
   router_id keepalived01
   vrrp_skip_check_adv_addr
   vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

# VRRP协议配置区域
# 初始状态支持 MASTER|BACKUP
# 如果priority 255 则会立即迁移
# 角色在至少接受3-4个 vrrp 组播或单播后状态会转换
vrrp_instance VI_1 {
    # 当前路由初始角色
    # 支持 MASTER|BACKUP
    state MASTER 
    # vrrp 绑定VIP接口
    # 单播模式下可以不指定
    interface eth0
    # vrrp 路由组
    # 同个组内IP必须一致 
    virtual_router_id 66
    # 优先级 
    # 优先级高的节点做master
    priority 100
    # vrrp消息发送时间秒为单位
    advert_int 1
    # VRRPV2中已经删除了此配置选项
    # 提供认证功能
    # 多播时防止接受到脏消息
    # 单播时可以不指定
    # 支持算法: PASS|AH
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    # 单播配置
    # 当前设备IP
    unicast_src_ip 133.133.1.10
    # 单播消息投递组
    # 可写多个
    unicast_peer {
	133.133.1.11	
    }
    # 虚拟服务VIP配置
    virtual_ipaddress {
	133.133.1.99/32	dev eth0 label eth0:0
    }
    # 消息通知机制
    # 当前vrrp切换到master时触发脚本
    # 注意脚本加执行权限
    notify_master "/etc/keepalived/alert.sh master VI_1:vip-133.133.1.99"
    # 消息通知机制
    # 当前vrrp切换到backup时触发脚本
    # 注意脚本加执行权限
    notify_slave "/etc/keepalived/alert.sh slave VI_1:vip-133.133.1.99"
}
vrrp_instance VI_2 {
    state BACKUP
    interface eth0
    virtual_router_id 77
    priority 80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1qaz@WSX
    }
    unicast_src_ip 133.133.1.10
    unicast_peer {
        133.133.1.11
    }
    virtual_ipaddress {
        133.133.1.88/32 dev eth0 label eth0:1
    }
    notify_master "/etc/keepalived/alert.sh master VI_1:vip-133.133.1.88"
    notify_slave "/etc/keepalived/alert.sh slave VI_1:vip-133.133.1.88"
}

virtual_server 133.133.1.99 80 {

	delay_loop 6
        lb_algo rr
        lb_kind DR
        protocol TCP
        # 此处的链接保持时间会导致rr模式不生效
        persistence_timeout 10
        real_server 133.133.1.20 80 {

		#weight 10
		HTTP_GET {

			http_protocol 1.0
			url {
			   path /
			   status_code 200
			}
                        connect_timeout 3
                        retry 3
                        delay_before_retry 3
		}

	}
       real_server 133.133.1.21 80 {
                HTTP_GET {
                        
                        http_protocol 1.0
                        url {
                           path /
                           status_code 200
                        }
                        connect_timeout 3
                        retry 3
                        delay_before_retry 3
                }
        
        }

}
```

##### 实践注意点：

###### rr模式不负载均衡:

```shell
0.先说大坑：为什么LVS设置了轮询，浏览器测试还是不能轮询？这关系到两个地方的配置：
  01./etc/keepalived/keepalived.conf的persistence_timeout会话保持时间配置，测试轮询时设置为0；
  02.查看ipvsadm默认超时时间（巨坑，导致我一直在浏览器刷不出LVS轮询，也是看到了参考文献3才知道的）[root@DR1 keepalived]# ipvsadm -L --timeout
Timeout (tcp tcpfin udp): 900 120 300

    900 120 300这三个数值分别是TCP TCPFINUDP的时间.也就是说一条tcp的连接经过lvs后,lvs会把这台记录保存15分钟，就是因为这个时间过长，所以很多人都会发现做好LVS DR之后轮询现象并没有发生，实践中将此数值调整很小小，使用以下命令调整：
[root@DR1 ~]# ipvsadm --set 1 2 1
    再次测试轮询效果，就可以了！而实际配置中还是按照默认配置，那么在大量IP访问VIP时，就有轮询效果？有待验证
```




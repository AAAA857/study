# Docker

## 容器简述:

```shell
  容器: 
     容器类似一个瓶子 是一个物品的载体，物品在载体内用于自己的独立空间，同时载体可以用于多个，每个载体都是独立的；同时载体内的物品于物品之间都是隔离的。
     
# 传统虚拟化和容器的区别？
   
   虚拟化:
   		1. 虚拟机是一个完整的操作系统，它运行在宿主机之上 Guest 模式运行
   		2. 虚拟机拥有独立的kernel，它不复用宿主机内核
   		3. 虚拟机拥有一个Hypervisor它可以允许多个虚拟机共享一个宿主机硬件资源
   		4. 虚拟机硬件资源在创建集群时就定义好
   		
   容器:
   		1. 容器没有完整的操作系统，它只是跑某一个应用程序
   		2. 容器没有独立的kernel ，它共享使用宿主机kernel
   		3. 容器是基于内核功能做资源隔离(namespace)
   		4. 容器销毁创建要快很多
   	    5. 容器的资源使用限制需要cgroup机制完成
   	
   	
# 容器技术带来的问题 多个容器公用一个kernel
	1. 如果解决进程隔离？
	2. 如何解决网络隔离？
	3. 如何解决主机名隔离？
	4. 如果解决文件存储问题？
	5  如何解决信号隔离？
	

# 资源隔离类型
1. 主机名域名 UTS
2. 根文件系统 Mount
3. 网络资源隔离 Network
4. 进程通信专用通道 IPC
5. 进程ID隔离	PID
6. 用户空间隔离 User
以上几种隔离在kernel中被namespace功能实现

```

![image-20240315152322142](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\image-20240315152322142.png)

## Docker网络:

```shell
   Net 名称中间主要做协议栈隔离，网卡采用虚拟网卡设备，采用软件方式模拟（二层和三层），二层工作在数据链路层，利用内核功能模拟一对网卡，一头插在虚拟主机内部，一头插在虚拟二层设备之上（虚拟交换机），软件交换机可以使用brctl创建。


# 常用网络运行模式

1、 桥接： 把物理网卡当交换机来使用
2、 NAT：  流量做NAT规则映射
3、 仅主机：


# overlay Network
  简称隧道网络，原则是在原始请求IP首部封装一层物理网络，不经过nat转换
  
# docker 网络
1. bridge
   在宿主机上创建一个虚拟网卡docker0，随后的每个一个容器为其分配一对网卡，一个在容器内，一个在docker0之上，默认走NAT规则。
2. host
   继承宿主机网络名称空间，
3. none
   容器不适用网络
```

### 实现网络隔离:

```shell
  linux 系统上可以创建出 net名称空间，并且可以通过ip link命令来创建一个一对虚拟网卡设备(veth),然后可以将网卡的两头防止到不同的netns 内，从而实现网络隔离。
 
 # 实现步骤
 # 创建俩个netns namespace
 
  ip netns help // 获取命令帮助

    $ ip netns add r1
    $ ip netns add r2
    $ ip netns list 
 # 查看新创建的netns内存在的网卡
    $ ip netns exec r1 ip addr show 
    
 # 创建虚拟 veth 设备
    $ ip link add name veth1.1 type veth peer name veth1.2
 
 # 将网卡防止在俩个netns 中
    $ ip link set dev veth1.1 netns r1
    $ ip link set dev veth1.2 netns r2 
  
 # 配置 r1 r2 veth设备IP并测试通信能力
    $ ip netns exec r1 ip address add 133.133.1.1/24 dev veth1.1
    $ ip netns exec r2 ip address add 133.133.1.2/24 dev veth1.2
    $ ip netns exec r1 ip link set dev veth1.1 up
    $ ip netns exec r2 ip link set dev veth1.2 up
    $ ip netns exec r1 ping 133.133.1.2
```

### Docker 支持的网络:

```shell
bridge	默认网络驱动程序。
host	移除容器和 Docker 主机之间的网络隔离。
none	将容器与主机和其他容器完全隔离。
overlay	Overlay 网络将多个 Docker 守护进程连接在一起。
ipvlan	IPvlan 网络提供对 IPv4 和 IPv6 寻址的完全控制。
macvlan	为容器分配 MAC 地址。

# 联合网络
docker run -d --name redis example/redis --bind 127.0.0.1

docker run --rm -it --network container:redis example/redis-cli -h 127.0.0.1
```

#### Bridge桥接模式:

```shell
# 什么是桥接
  1.bridge 对宿主机来讲相当于一个单独的网卡设备 对于运行在宿主机上的每个容器来说相当于一个交换机，所有容器的虚拟网线的一端都连接到docker0上。
  2.就网络而言，桥接网络是一种在网段之间转发流量的链路层设备。桥接器可以是硬件设备，也可以是在主机内核中运行的软件设备。
  3.Docker而言，桥接网络使用软件桥接，让连接到同一桥接网络的容器进行通信，同时提供与未连接到该桥接网络的容器的隔离。



# 创建bridge
 $ docker network create --subnet '180.10.0.0/16' --gateway 180.10.0.1 test-bridge
 
 # 修改网卡名称
 $ ip link set dev br-b501c8c7834f down 
 $ ip link set dev br-b501c8c7834f name docker1
 $ ip link set dev docker1 up
 
 # 创建容器
 $ docker container run -d -it --name busybox01 --net test-bridge  busybox
 $ docker container run -d -it --name busybox02 --net test-bridge  busybox
 
 # 查看桥接状态
 $ brctl show 
 
 
 # 为正在运行的容器修改网桥
 $ docker network connet <bridge Name> <容器名称>
 $ docker network disconnect  <bridge Name> <容器名称>
 
```

##### 配置默认网桥:

```shell
如果需要对默认docker0网桥做一些配置变更；例如变化IP等参考下面的配置
  
$ vim /etc/docker/dameon.json
    {
      "bip": "192.168.1.1/24",
      "fixed-cidr": "192.168.1.0/25",
      "fixed-cidr-v6": "2001:db8::/64",
      "mtu": 1500,
      "default-gateway": "192.168.1.254",
      "default-gateway-v6": "2001:db8:abcd::89",
      "dns": ["10.20.1.2","10.20.1.3"]
    }
 $ systemctl daemon-reload
 $ systemctl restart docker
 
```

#### Overlay网络:

**Underlay架构图**

![18565512884748e96dcb85ad2f9bec97.png](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\Underlay.jpg)

**Overlay架构图**

![u=1787878965,2260258850&fm=253&fmt=auto&app=138&f=PNG.webp](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\overlay架构.jpg)

```shell
# 术语
  Underlay: 底部衬托属于基础硬件设备 路由器、交换机等
  Overlay: 叠加网络 它依赖于Underlay网络之上实现
  
# Underlay网络概念
  Underlay是网络的基础设备，它主要有路由器、防火墙、汇聚交换机、核心交换机等众多设备组成。
  
# Underlay网络带来的问题
  网络的各个设备之间必须通过路由协议来确保之间 IP 的连通性。然而传统的网络设备对数据包的转发都基于硬件，其构建而成的 Underlay 网络也产生了如下的问题：
  1. 底层硬件跟进IP地址转发，对网络架构的要求严格
  2. 新增或者架构变更必须对现有的底层设备进行改造
  3. 硬件设备数据传输的安全性
  4. 网络切片、网络分区的复杂性
  
# Overlay网络概念
  Overlay 网络是通过网络虚拟化技术（软件的实现），在同一张 Underlay 网络上构建出的一张或者多张虚拟的逻辑网络。不同的 Overlay 网络虽然共享 Underlay 网络中的设备和线路，但是 Overlay 网络中的业务与 Underlay 网络中的物理组网和互联技术相互解耦。
  
  为了摆脱 Underlay 网络的种种限制，现在多采用网络虚拟化技术在 Underlay 网络之上创建虚拟的 Overlay 网络。
  
  
# 如何建立的Overlay网络
  相连的不通物理节点之上建立隧道网络(通过软件方式)，数据包在发送的前做数据报文封装，在原IP目的IP之上，新增一层IP首部和隧道首部且屏蔽掉内层的 IP 头部，数据包根据新的 IP 头部进行转发。当数据包传递到另一个设备后，外部的 IP 报头和隧道头将被丢弃，得到原始的数据包，在这个过程中 Overlay 网络并不感知 Underlay 网络。
  

# Overlay 实现的协议
  Overlay 网络有着各种网络协议和标准，包括 VXLAN、NVGRE、SST、GRE、NVO3、EVPN 等
```

##### Docker Overlay 网络模式

```shell
   Docker Overlay 网络是一种网络技术，它使用了 Docker 引擎的特性，使得多个 Docker 主机可以连接在一起，形成一个虚拟网络，从而实现多主机之间的容器通信。Docker Overlay 网络使用 VXLAN 协议实现跨主机的网络通信。

   Docker Overlay 网络是使用 VXLAN 协议实现的，VXLAN 是一种虚拟化隧道协议，它可以将二层网络封装在 UDP 包中传输，从而实现跨主机的网络通信

```

##### **Docker Overlay 网络的工作流程**

![1183448-20181102195641010-1957951065.png](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\dockerOverlay流程图)

```shell
# 工作流程介绍
  容器 Container1 如何发送数据包 到容器 Container2 ？
  1. 容器 Container1 会通过 Container eth0 将这个数据包发送到 10.0.0.1 的网关。   2. 网关将数据包发送出去后到达 br0 网桥。
  3. br0 网桥针对 VXLAN 设备，主要用于捕获对外的数据包通过 VETP 进行数据包封装。
  4. 封装好将 VXLAN 格式数据包交给 eth0，通过 UDP 方式交给 Container2 的 eth0。
  5. Container2 收到数据包后通过 VETP 将数据包解封装。
  6. 网桥通过网关将解封装的数据包转发给 Container eth0，完毕通信。
```



##### Docker配置Overlay网络:

###### 前提条件:

```shell
   Docker 默认如果使用Overlay网络的话需要使用到swarm，Swarm是Dcoker的集群管理工具，它可以将多个Docker独立主机组件成一个视图之下，通过Swarm管理主机来创建task，task会均衡部署到Swarm Node节点之上运行。
   
# Swarm角色组件
  swarm manager: 负责初始化swarm集群，负责管理任务调度、创建、销毁等生命周期管理
  swarm node:	 work节点负责调度业务
# Swarm网桥
  swarm ingress: Overlay模式，用来暴漏swarm中业务端口，对外访问，调用ipvs模块实现
  swarm docker_gwbridge: bridge模式，主要是对容器访问外部流量出口NAT模式
  
```

###### 初始化Swarm Manager:

**Swarm架构图**

![img](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\DockerSwarm架构图.png)

```shell
# 初始化集群
$ docker swarm init --advertise-addr 133.133.1.14 #这里的 IP 为创建机器时分配的 ip。
# 创建Overlay网桥
$ docker network create -d overlay --attachable my-attachable-overlay

# Node节点加入Swarm集群
$ docker swarm join \
--token SWMTKN-1-4oogo9qziq768dma0uh3j0z0m5twlm10iynvz7ixza96k6jh9p-ajkb6w7qd06y1e33yrgko64sk 192.168.99.107:2377

# Manager节点查看运行状态
$ docker node ls 
```

###### Docker运行Overlay容器:

###### **容器overlay通信抓包图**

![image-20240320132101226](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\over,ay网络抓包.png)

```shell
# Swarm 创建Service 服务
$  docker service create --replicas 2  --network my-network-overlay --name helloworld1 alpine  ping docker.com

--network 指向手动创建的overlay网桥
# 进入容器进行测试
$ ping 10.10.0.9

# 抓包分析
$ tcpdump -i eth0 port 4789 -nnnvvv
```

#### Host模式:

```shell
  host 容器的网络堆栈不会与 Docker 主机隔离（容器共享主机的网络命名空间），并且容器不会分配自己的 IP 地址。例如，如果您运行绑定到端口 80 的容器并且使用host 网络，则该容器的应用程序可在主机 IP 地址的端口 80 上使用。


# 注意
  在使用Host网络模型下，—-publish-all -P -p 都将不生效，因为已经在物理机暴漏所有容器端口
  

# host模式优点
  1. 性能更好不经过overlay或iptables的转发
  2. 在容器需要大规模端口暴漏情况下
 

# host模式运行容器
$ docker run -it --name host-container-test --net host nginx:last
$ netstat -utpln |grep 80
```

#### IPVlan模式:

```shell
# 先决条件
1. 节点都是单独的docker物理机
2. 内核要求需要kernel > v4.2版本 
   IPvlan Linux 内核 v4.2+（存在对早期内核的支持，但存在错误）。要检查当前的内核版本，请使用uname -r
   
   
# IPvlan
IPvlan 模式支持 L2层和L3层， L2层通过MAC地址转发，要求容器的网段需要跟物理机在同网段，他能通过不通vlan来做访问限制，同时实现跨节点操作。

IPvlan 是经过考验的真实网络虚拟化技术的新变化。Linux 实现非常轻量级，因为它们不是使用传统的 Linux 桥进行隔离，而是与 Linux 以太网接口或子接口相关联，以强制网络之间的分离以及与物理网络的连接。

IPvlan 提供了许多独特的功能，并为各种模式的进一步创新提供了充足的空间。这些方法的两个高级优势是，绕过 Linux 桥的性能影响以及部件较少的简单性。移除传统上位于 Docker 主机 NIC 和容器接口之间的桥接器，留下由直接连接到 Docker 主机接口的容器接口组成的简单设置。面向外部的服务很容易访问此结果，因为在这些场景中不需要端口映射。
```

##### IPvlan L2配置:

**L2层架构图**

![简单 IPvlan L2 模式示例](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\IPVlan模式架构图.png)

```shell
# 配置步骤
1. 所有docker节点均要升级内核 >v4.2版本
2. 所有docker可以创建独立的vlan 或者直接继承 eth0 如果继承eth0 表示使用默认vlanID
3. 所有容器均要--net 引用 IPvlan Network
```

###### Kernrl升级内核：

```shell
# 关于内核种类:
   kernel-ml——kernel-ml 中的ml是英文【 mainline stable 】的缩写，elrepo-kernel中罗列出来的是最新的稳定主线版本。

   kernel-lt——kernel-lt 中的lt是英文【 long term support 】的缩写，elrepo-kernel中罗列出来的长期支持版本。ML 与 LT 两种内核类型版本可以共存，但每种类型内核只能存在一个版本。

# 升级kernel
$ uname -a   //仅查看版本信息
$ uname -r
#  通过绝对路径查看查看版本信息及相关内容
$ cat /proc/version
#  通过绝对路径查看查看版本信息
$ cat /etc/redhat-release


# 更新机器软件包版本
$ yum -y update
# 导入Kernel epel源
$ rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
# 安装ELRepo仓库的yum源
$ yum install https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm
# 查询可用内核版本
$ yum --disablerepo="*" --enablerepo="elrepo-kernel" list available

# 安装 LT 版本，K8S全部选这个
$ yum --enablerepo=elrepo-kernel install kernel-lt-devel-5.4.225-1.el7.elrepo.x86_64 kernel-lt-5.4.225-1.el7.elrepo.x86_64 -y


# 修改kernel加载项
$ grub2-set-default 0

# 重启
$ reboot
```

###### Docker IPvlan L2:

**抓包图**

![image-20240321110914388](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\ipvlan抓包图.png)

```shell
# 划分Vlan
# 如果直接继承eth0 那么容器将跟整个网段共享同vlan
# 创建vlan10
$ ip link add link eth0 name eth0.10 type vlan id 10
$ ip link set eth0.10 up

# 创建IPvlan network
$  docker network create --driver ipvlan --subnet=133.133.1.0/24 --gateway=133.133.1.1 -o ipvlan_mode=l2 -o parent=eth0.10 db_net

# 运行docker 测试
# 在不通机器上运行
$ docker run --net=db_net --ip 133.133.1.2 -it --rm alpine /bin/sh
$ docker run --net=db_net --ip 133.133.1.3 -it --rm alpine /bin/sh

# 测试
# exec 到容器后仅能ping同在同vlan节点IP，其余的都不通
$ ping 133.133.1.1 //不通
$ ping 133.133.1.3 //通
```

###### IPVlan L3配置:

![Docker IPvlan L2 模式](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\ipvlan-l3.webp)

```shell
 	L3 模式可以在单台docker 主机上实现路由模式，容器与容器之间可以非同网段，不能跨主机通信如果需要通信需要加中间路由器。
 	IPvlan L3 模式会丢弃所有广播和组播流量。仅这个原因就使得 IPvlan L3 模式成为那些寻求大规模和可预测网络集成的人的主要候选者。
 	

# 创建L3 IPVlan Network
$ docker network create -d ipvlan \
    --subnet=192.168.214.0/24 \
    --subnet=10.1.214.0/24 \
    -o ipvlan_mode=l3 ipnet210
    
# 运行容器测试
$ docker run --net=ipnet210 --ip=192.168.214.10 -itd alpine /bin/sh
$ docker run --net=ipnet210 --ip=10.1.214.10 -itd alpine /bin/sh
  
  
$ docker run --net=ipnet210 --ip=192.168.214.9 -it --rm alpine ping -c 2 10.1.214.10

$ docker run --net=ipnet210 --ip=10.1.214.9 -it --rm alpine ping -c 2 192.168.214.10
 	
   为了从远程 Docker 主机 ping 容器或者容器能够 ping 远程主机，远程主机或之间的物理网络需要有一条路由指向容器的 Docker 主机 eth 接口的主机 IP 地址。
```

## Docker 存储卷:

### Overlay2存储:

#### 联合挂载技术:

![image-20240322104918417](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\联合挂载.png)

```shell
   联合挂载技术（Union Mount），就是将原有的文件系统中的不同目录进行合并（merge），最后向我们呈现出一个合并后文件系统。在 overlay2 文件结构中，联合挂载技术通过联合三个不同的目录来实现：lower目录、upper目录和work目录，这三个目录联合挂载后得到merged目录
   
   
# 目录含义
  lower: 基础层可以是多个组合到一起
  upper: 读写层只有一个
  work:  工作基础目录，挂载后会被清空，使用过程中其内容不可见
  merge: 联合挂载后统一展示的试图，就是最终合并完成的效果
```

#### 手动验证联合挂载系统:

```shell
# 创建验证所需的lower目录
  mkdir lowerA lowerB uper worker mount_test
# 创建文件
  echo "FROM lower A" >> lowerA/a.txt
  echo "FROM lower A" >> lowerA/b.txt
  echo "FROM lower A" >> lowerA/c.txt 
 
  echo "FROM lower B" >> lowerB/b.txt

  echo "FROM lower C" >> lowerC/a.txt
  echo "FROM lower C" >> lowerC/c.txt 
  
  echo "FROM upper" >> upeer/a.txt
# 挂载
  mount -t overlay overlay -o lowerdir=./lowerA:./lowerB,upeerdir=./uper,workdir=./woker ./mount_test
  
# 验证
  cd ./mount_test
  tree
        .
        ├── a.txt		//来着upeer层
        ├── b.txt		//来着lowerA
        ├── c.txt		//来自lowerA
        
     
```

#### merged修改文件:

```shell
	merged层修改的文件，如果文件来自lower层会通过“写时复制”方式将文件复制一份到upeer层，此时的修改是在upeer层完成的，对底层的lower层来说是无感知的。
	
# 测试
  cd mount_test/merged
  cp /etc/hosts ./
  echo "abc" >> ./a.txt
```

**验证截图**:

*merged层:*

![image-20240322110939177](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\image-20240322110939177.png)

*upper层:*

![image-20240322111045435](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\image-20240322111045435.png)

![image-20240322111159127](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\image-20240322111159127.png)



#### overlay删除文件:

```shell
# 实验动作
  cd merged
  rm -rf a.txt
  
# 结论
 1. 当在merged层删除a.txt后merge层将看到的是文件已经不存在（非真正意义上的删除）
 2. upper层可以看到多了一个a.txt，可以说明在merge层的操作实际都是保存在upper层中的
 3. lowe A目录中a.txt依然存在不受其影响，只读模式

# 为什么文件没删除而merge层却看不到？
  whiteout: 概念存在于联合文件系统（UnionFS）中，代表某一类占位符形态的特殊文件，当用户文件夹与系统文件夹的共通部分联合到一个目录时（例如 bin 目录），用户可删除归属于自己的某些系统文件副本，但归属于系统级的原件仍存留于同一个联合目录中，此时系统将产生一份 whiteout 文件，表示该文件在当前用户目录中已删除，但系统目录中仍然保留。
```

![image-20240322111617699](C:\Users\THINKPAD\AppData\Roaming\Typora\typora-user-images\image-20240322111617699.png)



```shell
 overlay2（分层式联合挂载） 是基于overlay的升级版本俩者使用的存储驱动都是OverlayFS。

 overlay  2014年首次被docker使用
 overlay2 2016年被合并在docker 1.12版本中引用，主要是修复了overlay中inode耗尽问题
 
 




```



## Docker 镜像加速:

**未开启镜像加速**

![image-20240319175526512](C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\git_repostry\study\学习文档\SRE学习\Docker\图片\image-20240319175526512.png)

```shell
   由于运营商网络原因，会导致您拉取Docker Hub镜像变慢，甚至下载失败。为此，阿里云容器镜像服务ACR提供了官方的镜像加速器，从而加速官方镜像的下载。
# 阿里云加速地址   
  https://cr.console.aliyun.com/spm=a2c4g.11186623.0.0.27881d82Wu4rws

  登录容器镜像服务控制台，在左侧导航栏选择镜像工具 > 镜像加速器，在镜像加速器页面获取加速器地址。 
# 配置加速器
$ sudo mkdir -p /etc/docker
$ sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://iokrz8u0.mirror.aliyuncs.com"]
}
$ EOF
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```


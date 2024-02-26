
'''
    logstash 将监听在本机的UDP，接收发送端发送的数据
'''
'''
input {
        udp{
                port => 25826
                buffer_size => 1452
                workers => 3          # Default is 2
                queue_size => 30000   # Default is 2000
                codec => collectd { }       // collectd 专用的编码器，解析数据
                type => "collectd"
        }

}
output {

        stdout {}
}
'''


'''
# 性能监控 collectd
# 收集机器 cpu、memory、disk、network、varnish、ceph 等等信息
# 使用udp协议

# 安装
yum -y install libcurl libcurl-devel rrdtool rrdtool-devel perl-rrdtool rrdtool-prel libgcrypt-devel gcc make gcc-c++ liboping liboping-devel perl-CPAN net-snmp net-snmp-devel
wget http://collectd.org/files/collectd-5.4.1.tar.gz --no-check-certificate
tar -axvf collectd-5.4.1.tar.gz -C /usr/local/collectd
 ./configure --prefix=/usr/local/software/collectd --sysconfdir=/etc --localstatedir=/var --libdir=/usr/lib --mandir=/usr/share/man --enable-all-plugins

 make && make install
cp /usr/local/collectd/sbin/collectd /usr/sbin/
 
 # 配置文件
 vim /etc/collectd.conf
Hostname "master03"
LoadPlugin interface
LoadPlugin cpu
LoadPlugin memory
LoadPlugin network
LoadPlugin df
LoadPlugin disk
<Plugin interface>
    Interface "enp130s0f0"
    IgnoreSelected false
</Plugin>
<Plugin network>
    <Server "127.0.0.1" "25826"> // 此处的IP 端口为UDP信息，对应logstash UDP 插件 监听的IP和端口
    </Server>
</Plugin>

# 启动
/usr/sbin/collectd -C /etc/collectd.conf

'''
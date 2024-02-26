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
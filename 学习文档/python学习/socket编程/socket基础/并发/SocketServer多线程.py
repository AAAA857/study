import socketserver

'''
    socketserver 封装了socket和对应的多线程方法

    socketserver 具有4个基础实体服务类：
    
        class socketserver.TCPServer()      //实现TCP流式传输
        class socketserver.UDPServer()      //实现UDP无边界数据传输
        
        # 这两个更常用的类与 TCP 和 UDP 类相似，但使用 Unix 域套接字；它们在非 Unix 系统平台上不可用。 它们的形参与 TCPServer 的相同。
        class socketserver.UnixStreamServer()       
        class socketserver.UnixDatagramServer()     
        
    
    四个基础服务类继承关系:
            +------------+
            | BaseServer |
            +------------+
                  |
                  v
            +-----------+        +------------------+
            | TCPServer |------->| UnixStreamServer |
            +-----------+        +------------------+
                  |
                  v
            +-----------+        +--------------------+
            | UDPServer |------->| UnixDatagramServer |
            +-----------+        +--------------------+
    
    TCPServer 源码分析执行流程:
        1. 实例化一个TCPServer 对象 "tcpserver"
        
            """按照下方代码分析此处主要做tcpserver的socket对象初始化，并且完成了tcp listen()、bind()"""
            tcpserver =  socketserver.TCPServer((HOST, PORT), MySocketServer)   
            
            """
                8. 执行tcpserver.server_forever()方法对应流程如下：
                    8.1 首先寻找TCPServer类中是否存在server_forever，如果不存在将会寻找继承的父类方法BaseServer   
                    8.2 TCPServer类中不存在查找父类代码如下
                            def serve_forever(self, poll_interval=0.5):
                                    """Handle one request at a time until shutdown.
                            
                                    Polls for shutdown every poll_interval seconds. Ignores
                                    self.timeout. If you need to do periodic tasks, do them in
                                    another thread.
                                    """
                                    self.__is_shut_down.clear()
                                    try:
                                        # XXX: Consider using another file descriptor or connecting to the
                                        # socket to wake this up instead of polling. Polling reduces our
                                        # responsiveness to a shutdown request and wastes cpu at all other
                                        # times.
                                        8.3: 此处实例化出一个selector对象并注册了self完成了多线程
                                        with _ServerSelector() as selector:
                                            selector.register(self, selectors.EVENT_READ)
                                            
                                            
                                            8.4： Not self.__shutdown_request=False 进入循环
                                            while not self.__shutdown_request:
                                                8.5 select 监听的socket是否有数据
                                                ready = selector.select(poll_interval)
                                                # bpo-35017: shutdown() called during select(), exit immediately.
                                                
                                                if self.__shutdown_request:
                                                    break
                                                    
                                                if ready:
                                                    8.6 执行tcpserver _handle_request_noblock() 方法 ->BaseServer._handle_request_noblock() 方法
                                                          """Handle one request, without blocking.

                                                            I assume that selector.select() has returned that the socket is
                                                            readable before this function was called, so there should be no risk of
                                                            blocking in get_request().
                                                            """
                                                            
                                                            try:
                                                                8.7 执行tcpserver的get_requets()方法 -> TCPServer.get_requests()方法代码如下:
                                                                         def get_request(self):
                                                                            """Get the request and client address from the socket.
                                                                    
                                                                            May be overridden.
                                                                    
                                                                            """
                                                                            8.8: 返回socket.accept() ,返回元组 client数据、client addr
                                
                                                                            return self.socket.accept()
                                                                            
                                                                8.9: 返回socket.accept()
                                                                    request = conn
                                                                    client_address = 客户端连接信息addr
                                                                request, client_address = self.get_request()
                                                            except OSError:
                                                                return
                                                           
                                                                    """
                                                                     8.10： self.verify_request 返回True BaseServer.verify_request() 代码如下
                                                                             def verify_request(self, request, client_address):
                                                                                    """Verify the request.  May be overridden.
                                                                            
                                                                                    Return True if we should proceed with this request.
                                                                            
                                                                                    """
                                                                                    return True
                                                                    """
                                                            if self.verify_request(request, client_address):
                                                                try:
                                                                        """
                                                                        8.11: if True语句成立将会执行self.process_request(request, client_address)
                                                                             
                                                                        8.12: 经过查找将会执行TCPServer 父类BaseServer.process_request 方法
                                                                              def process_request(self, request, client_address):
                                                                                    """Call finish_request.
                                                                            
                                                                                    Overridden by ForkingMixIn and ThreadingMixIn.
                                                                            
                                                                                    """
                                                                                    8.13： 执行tcpserver的finish_request(equest, client_address)方法
                                                                                    8.14:  TCPServer -> BaseServer.finish_request(equest, client_address) 方法
                                                                                    8.15： finish_request 代码如下：
                                                                                                def finish_request(self, request, client_address):
                                                                                                        """Finish one request by instantiating RequestHandlerClass."""
                                                                                                        8.16: 执行tcpserver的self.RequestHandlerClass(request, client_address, self)
                                                                                                        8.17: 此处执行的self.RequestHandlerClass 等于第一步赋值的自定义hanlder方法
                                                                                                        self.RequestHandlerClass(request, client_address, self)
                                                                                    self.finish_request(equest, client_address)
                                                                                    self.shutdown_request(request)      
                                                                                
                                                                                
                                                                                
                                                                        """
                                                                    self.process_request(request, client_address)
                                                                except Exception:
                                                                    self.handle_error(request, client_address)
                                                                    self.shutdown_request(request)
                                                                except:
                                                                    self.shutdown_request(request)
                                                                    raise
                                                            else:
                                                                self.shutdown_request(request)
  
                                                     8.10: 此处完成了组测request、client_address俩个属性
                                                    self._handle_request_noblock()
                                                    
                                                8.11： 执行tcpserver.service_actions()方法
                                                self.service_actions()  
                                    finally:
                                        # 执行完注册一个__shutdown_request = False 私有属性
                                        self.__shutdown_request = False
                                        self.__is_shut_down.set()                 
            """                     
            tcpserver.serve_forever()
        2. 执行TCPServer __init__方法 
            """
                    1. 接收2个参数
                        server_address = (IP,PORT)
                        RequestHandlerClass = 自定义的hanlder方法类    
                        bind_and_activate = True 默认值用于下方的if判断语句
               """
            def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
               
               """
                 2. 执行父类的__init__构造方法不进行覆盖继承方式
                        def __init__(self, server_address, RequestHandlerClass):
                            """Constructor.  May be extended, do not override."""
                            # tcpserver 实列赋值 server_address = (IP,PORT)
                            self.server_address = server_address
                            # tcpserver 实例赋值    RequestHandlerClass = 自定义的hanlder方法类
                            self.RequestHandlerClass = RequestHandlerClass
                            
                            # 多线程相关
                            self.__is_shut_down = threading.Event()
                            self.__shutdown_request = False
               """
                BaseServer.__init__(self, server_address, RequestHandlerClass)
                
                """
                 3. 为tcpserver 实例化一个socket 对象实例属性
                     self.address_family = socket.AF_INET           // 网络协议
                     self.socket_type = socket.SOCK_STREAM          // TCP协议
                """
                self.socket = socket.socket(self.address_family,
                                            self.socket_type)
                                            
                                            
                """
                    4. bind_and_active 在TCPServer __init__实例属性默认为True 进入对应的执行逻辑代码块
                """
                if bind_and_activate:
                    """ 
                        5. 创建一个异常处理
                            5.1:如果出现异常将会except捕获执行流程如下:
                                5.1.1：检查tcpserver自己的实例属性中是否存在server_close()执行方法
                                5.1.2：tcpserver不存在server_close方法 --> TCPServer 父类 
                                5.1.3: TCPServer父类存在server_close方法执行对应方法 
                                5.1.4: 方法如下:
                                        def server_close(self):
                                            """Called to clean-up the server.
                                    
                                            May be overridden.
                                    
                                            """
                                            # 此时的self 为tcpserver 实例对象，将会执行socket自带的close()方法关闭socket实例
                                            self.socket.close()
                            5.2:正常逻辑不存在异常执行流程如下:
                                5.2.1: self = tcpserver 执行server_bind()方法
                                5.2.2： 查找tcpserver实例属性是否存在server_bind方法
                                5.2.3： tcpserver __dir__ 中存在server_bind方法将会执行server_bind() 对应代码如下
                                            def server_bind(self):
                                                """Called by constructor to bind the socket.
                                        
                                                May be overridden.
                                        
                                                """
                                                if self.allow_reuse_address and hasattr(socket, "SO_REUSEADDR"):
                                                    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                                if self.allow_reuse_port and hasattr(socket, "SO_REUSEPORT"):
                                                    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                                                    
                                                    
                                                5.2.4：执行socket.bind((IP,PORT)),到此TCP的绑定IP地址流程完成
                                                self.socket.bind(self.server_address)
                                                self.server_address = self.socket.getsockname()
                    """
                    try:
                        self.server_bind()
                        
                        """
                            6. 执行tcpserver的server_activate()方法流程如下：
                                6.1 在tcpserver自己的实例方法中寻找server_activate方法，如果不存在将寻找类的父类方法
                                6.2 寻找到方法server_activate（）对应代码如下
                                        def server_activate(self):
                                            """Called by constructor to activate the server.
                                    
                                            May be overridden.
                                    
                                            """
                                            6.3 执行socket.listen（）方法设置socket连接池初始值大小
                                                request_queue_size = 5  初始值为5
                                            
                                            self.socket.listen(self.request_queue_size)
                        
                        """
                        self.server_activate()
                        7. 到此tcpserver的socket对象实例化完毕
                    except:
                        self.server_close()
                        raise
'''

class MySocketServer(socketserver.BaseRequestHandler):

    def handle(self):

        self.data = self.request.recv(1024).strip()

        print("{} wrote:".format(self.client_address[0]))

        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
    def finish(self):
        """"""
if __name__ == '__main__':
    HOST, PORT = "localhost", 9999
    # Create the server, binding to localhost on port 9999
    # with socketserver.TCPServer((HOST, PORT), MySocketServer) as server:
    #     # Activate the server; this will keep running until you
    #     # interrupt the program with Ctrl-C
    #     server.serve_forever()
    '''
        TCPServer __init__：
            def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
                self = 实例化对象
                server_address = (ip,port)
                RequestHandlerClass = 自定义handler方法类
    '''

    tcpserver = socketserver.TCPServer(server_address=(HOST,PORT),RequestHandlerClass=MySocketServer)
    print(tcpserver.__dir__())
    tcpserver.serve_forever()
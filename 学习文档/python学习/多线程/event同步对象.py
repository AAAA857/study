'''
    同步对象: A B双线程在执行任务时需要同步消息，A 执行完成要发出信息 B接收到信号继续往下执行
'''
'''
    event = threading.Event()   // 实例event对象
    event.wait //等待消息不往下执行
    event.set  //设置一个event
    event.clear //清空event
'''
import threading
import time

Event = threading.Event()
def boss():
    global Event
    print('今天要加班')
    # 设置一个event
    Event.set()
    time.sleep(20)
    print('可以下班了')
    Event.set()

def work():
    global Event
    # 等待event.set被设定
    Event.wait()
    print('命苦呀！！')
    time.sleep(2)
    # 清空event 进入wait状态
    # 等待下次event.set后再次执行后面代码
    Event.clear()
    Event.wait()
    print('太开心了')

if __name__ == '__main__':
    '''
        执行流程:
            boss 执行函数打印消息，然后设置了一个event.set()
            work 首先在进行等待 event.wait()
            work 接收到set()事件后开始执行
            work 代码执行完成后清空event.clear()
            work 再次进入wait()
            boss 再次执行event.set()
            work 接收到事件开始执行阻塞代码
    '''

    Thread = []
    b1 = threading.Thread(target=boss).start()
    w1 = threading.Thread(target=work).start()
    w2 = threading.Thread(target=work).start()
    Thread.append(b1)
    Thread.append(w1)

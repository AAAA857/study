'''
    queue: 队列是用来多线程之间数据通信传输的
        队列模式:
            1. 先进先出 queue.Queue()
            2. 后进先出 queue.LifoQueue()
            3. 优先级   queue.PriorityQueue()
'''
'''
    queue 使用方法:
        queue.Queue(size)   //实例化队列
        queue.Queue.put()   //队列新增一条数据
        queue.Queue.get()   //队列中获取一条数据没有设置blok=true将阻塞
        queue.Queue.qsize() //打印当前队列条目数
        queue.Queue.empty() //判断队列是否为空
        queue.Queue.full()  //根据size定义来判断队列是否满了
        queue.Queue.get_nowait()    //不阻塞相当于get(block=false)
        queue.Queue.put_nowait（）   //当size满了后put会阻塞使用此方法会报错queue full
        queue.Queue.task_done()     //函数向任务已完成的队列发出一个信号
        queue.Queue.join()          //意味着队列为空时在执行其他任务
'''

import threading
import queue
import time
number = [i for i in range(20)]
def foo(q1,q2):
    global number
    while True:
        if len(number) == 0:
            break
        index = number[-1]
        print(index)
        time.sleep(0.1)
        number.remove(index)
        q1.put(number)
        number = q2.get()
def bar(q1,q2):
    while True:
        if len(number) == 0:
            break
        a = q1.get()
        print('线程2接收了%s',(a))
        index = a[-1]
        print(index)
        time.sleep(0.1)
        number.remove(index)
        q2.put(number)


def bar_priority_queue(q):

    q.put([2,11])
    q.put([3,12])
    q.put_nowait([1,999])

    while True:

        if q.qsize():
            print(q.get())
        else:
            break

if __name__ == '__main__':
    Thread = []
    # q1 = queue.Queue()
    # q2 = queue.Queue()
    # t1 = threading.Thread(target=foo,args=(q1,q2)).start()
    # t2 = threading.Thread(target=bar,args=(q1,q2)).start()
    q = queue.PriorityQueue(maxsize=2)
    print(bar_priority_queue(q))
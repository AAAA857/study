'''
    死锁：多线程在使用到多把一样的锁时因为延迟或阻塞导致双方都在等待释放
'''
'''
    递归锁Rlock: 死锁的解决方案,次锁是通过tag方式来探测如果锁没被释放不会进行申请锁绑定
'''

import threading
import time
class foo(threading.Thread):
    '''死锁案例'''

    def actionA(self):
        lock_a.acquire()
        print(self.name,'ActionA-1',time.ctime())
        time.sleep(2)
        lock_b.acquire()
        print(self.name,'ActionA-2',time.ctime())
        time.sleep(1)
        lock_a.release()
        lock_b.release()

    def actionB(self):
        lock_b.acquire()
        print(self.name, 'ActionB-1', time.ctime())
        time.sleep(1)
        # 多线程同步锁此处会出现死锁
        lock_a.acquire()
        print(self.name, 'ActionB-2', time.ctime())
        lock_b.release()
        lock_a.release()
    def run(self):
        self.actionA()
        self.actionB()
        return True
class bar(threading.Thread):

    '''递归锁'''
    def actionA(self):
        Rlock.acquire()
        print(self.name,'ActionA-1',time.ctime())
        time.sleep(2)
        Rlock.acquire()
        print(self.name,'ActionA-2',time.ctime())
        time.sleep(1)
        Rlock.release()
        Rlock.release()

    def actionB(self):
        Rlock.acquire()
        print(self.name, 'ActionB-1', time.ctime())
        time.sleep(1)
        # 多线程同步锁此处会出现死锁
        Rlock.acquire()
        print(self.name, 'ActionB-2', time.ctime())
        Rlock.release()
        Rlock.release()
    def run(self):
        self.actionA()
        self.actionB()
        return True
if __name__ == '__main__':
    '''
        执行流程步骤:
          Thread-1 ActionA-1 Fri Mar  1 12:43:19 2024  
            1. 此处第一个线程申请到了lock_a，其他线程在等待lock_a锁释放之后在运行等待状态
            2. 睡眠2秒后获取lock_b锁打印了下面，此时线程1 同时拥有2把锁不会释放（lock_a && lock_b）
            Thread-1 ActionA-2 Fri Mar  1 12:43:21 2024
            3, 睡眠1秒后线程1开始释放锁：
                3.1 先释放lock_a锁，此时的第二个线程检测到lock_a被释放开始执行ActionA函数
                3.2 后释放了lock_b锁
            4. 线程1的ActionB开始执行并获取了lock_b锁没有释放打印如下
               Thread-1 ActionB-1 Fri Mar  1 12:43:22 2024
                4.1 此时ActionB 在睡眠2秒后开始获取lock_a 锁
                4.2 此时的ActionB 需要获取到lock_a锁但是已经被线程2获取到无法执行 --->此处出现死锁        
            5. 线程2在线程1的lock_a锁释放的同时也开始了运行
                5.1 线程2 ActionA获取到了lock_a锁打印如下
                 Thread-2 ActionA-1 Fri Mar  1 12:43:22 2024
                5.2 线程2 ActionA现在需要获取lock_b锁，但是已经被线程1中的ActionB获取到无法执行 -->此处出现死锁
            6. 在线程1没有释放lock_b和线程2没有释放lock_a锁时就出现了死锁；程序无法执行
    '''
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    Rlock = threading.RLock()
    Thread = []
    for i in range(2):
        obj = bar()
        obj.start()
        Thread.append(obj)
    for n in Thread:
        n.join()
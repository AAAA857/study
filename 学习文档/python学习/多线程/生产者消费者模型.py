import threading
import time
import queue

'''
    包子铺：
        生产者负责生产包子，消费者根据生产的包子进行消费
'''
num  = 100
class production(threading.Thread):
    def __init__(self,q):
        super().__init__()
        self.q = q
        self.Lock = threading.RLock()
    def run(self):
        global num
        while True:
            if num == 0:
                break
            self.Lock.acquire()
            print(self.name,'生产包子+1')
            q.put(num)
            time.sleep(1)
            num -= 1
            self.Lock.release()
class consumer(threading.Thread):
    def __init__(self,q)0:
        super().__init__()
        self.q = q
    def run(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                print(self.name,'吃了包子： %s'%(data))
            else:
                print('包子都吃完了！')
                time.sleep(3)


if __name__ == '__main__':

    q = queue.Queue()
    p1 = production(q=q).start()
    p2 = production(q=q).start()
    p3 = production(q=q).start()
    c1 = consumer(q=q).start()

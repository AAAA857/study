'''

    信号量:
        1. 控制线程并发数
        2. threading.Semaphore(5)内部通过计数器方式每当调用acquire时从池子里面-1
        每当调用release()时信号量线程池+1

'''
import threading
import time
Semaphor = threading.Semaphore(5)



def stop_car():
    global Semaphor

    if Semaphor.acquire():
        print('停车1')
        time.sleep(5)
        Semaphor.release()

if __name__ == '__main__':
    Thread = []
    for i in range(50):
        t = threading.Thread(target=stop_car)
        t.start()
        Thread.append(t)
    for T in Thread:
        T.join()



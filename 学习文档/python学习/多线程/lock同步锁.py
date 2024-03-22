'''
    1. 多线程模式下如果一个任务同一时刻去处理一个变量；
    如果执行过程中遇到阻塞；或者有时间延迟会造成结果不一致。
'''
import threading
import time

number = 100
'''
    下方代码在多线程同时操作变量做减一操作时当有延迟的时候由于cpu
特性遇到阻塞就切换，那么下一个线程在拿到的内存中变量将是一个没有
发送变化的值

'''

'''
    线程锁: 处理多线程模式数据共享不安全场景，例如多个线程同时都需要修改某个参数
    
    线程锁使用方法:
        threading.Lock()    //实例出一把锁次
        threading.Lock.acquire()    //加锁
        threading.Lock.release()    //释放锁
        
'''
def bar():
    '''
        未加锁案例:
            如果有一点延迟那么得到的number结果就不是一个自己想要的

    :return:
    '''
    global number
    a = number
    a -= 1
    time.sleep(0.01)
    number = a
    return number

def foo():

    '''
        加锁案例


    :return:
    '''
    global lock1
    global number
    if lock1.acquire():
        a = number
        a -= 1
        time.sleep(0.1)
        number = a
        # 加锁的任务执行完成后需要释放锁
        # 如果不释放其他线程将不能正常执行
        lock1.release()
    return number
if __name__ == '__main__':
    Thread = []
    # 获取一个线程锁
    lock1 = threading.Lock()
    for i in range(0,100):
        t = threading.Thread(target=foo)
        t.start()
        Thread.append(t)

    for n in Thread:
        n.join()
    print(number)


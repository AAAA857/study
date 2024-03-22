'''
    python gil锁限制了多线程程只能使用单核CPU，为了利用多cpu特性 启动多个进程来弥补
'''
'''
    Process 模块方法:
        start()   启动进程
        join()    等待程序执行完成
        

'''
from multiprocessing import Process
import threading
import time
def Count_Number(number):

    n = 0
    start_time = time.time()
    for i in range(number):
        n +=1
    print("并发线程顺序执行total_time: {}".format(time.time() - start_time))
    return n

if __name__ == '__main__':
    P = []

    for i in range(2):
        process_work = Process(target=Count_Number,args=(1000000000,))
        process_work.start()
        P.append(process_work)

    for n in P:
        n.join()

    print('end')



   # Thread = []
   # for i in range(2):
   #     t = threading.Thread(target=Count_Number,args=(1000000000,))
   #     t.start()
   #     t.join()
   #单线程顺序执行total_time: 69.13427543640137
   #单线程顺序执行total_time: 73.86708641052246

   # Thread = []
   # for i in range(2):
   #     t = threading.Thread(target=Count_Number, args=(1000000000,))
   #     t.start()
   #     Thread.append(t)
   # for n in Thread:
   #     n.join()
   #并发线程顺序执行total_time: 129.28987383842468
   #并发线程顺序执行total_time: 129.46963262557983

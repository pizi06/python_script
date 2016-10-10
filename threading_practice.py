# -*- coding:utf8 -*-
'''
require python3.5
'''

import threading
import time

########################################base###################################
def base(arg):
    time.sleep(1)
    print("thread" + str(arg) + "\r\n")

def test_base():
    for i in range(10):
        t = threading.Thread(target=base, args=(i,))
        t.start()
        print("t name: %s" % t.getName())

    print("main thread stop")

##################################自定義線程累#################################

class MyThreading(threading.Thread):
    '''
    对于threading模块中的Thread类，本质上是执行了它的run方法。
    因此可以自定义线程类，让它继承Thread类，然后重写run方法。

    Thread类的主要方法：
    join:
    它的存在是告诉主线程，必须在这个位置等待子线程执行完毕后，
    才继续进行主线程的后面的代码。但是当setDaemon为True时，join方法是无效的。
    '''
    def __init__(self, func, arg):
        super(MyThreading, self).__init__()
        self.func = func
        self.arg = arg

    def run(self):
        self.func(self.arg)

def f1(args):
    print(args)

def test_mythreading():
    obj = MyThreading(f1, 124)
    obj.start()

##################################鎖(未加鎖)#################################
NUM = 0
def show():
    '''
    未加鎖，出現臟數據
    '''
    global NUM
    NUM += 1
    name = threading.currentThread().getName()
    # 注意，这行语句的位置很重要，必须在NUM被修改后，否则观察不到脏数据的现象。
    time.sleep(1)
    print(name, "執行完畢后，NUM的值為：", NUM)

def test_show():
    for i in range(10):
        t = threading.Thread(target=show)
        t.start()
    print("main thread stop")

##################################鎖(加鎖)#################################
NUM = 10
def func(lock, i):
    global NUM
    # lock.acquire() # 讓鎖起作用
    NUM -= 1
    time.sleep(1)
    print("i: %s, NUM: %d" % (i, NUM))
    # lock.release() # 釋放鎖

def test_func():
    # Lock类，它不支持嵌套锁。
    # RLcok类的用法和Lock一模一样，但它支持嵌套，因此我们一般直接使用RLcok类。
    lock = threading.RLock() # 實例化一個鎖對象
    for i in range(10):
        t = threading.Thread(target=func, args=(lock,i))
        t.start()

##############################鎖(semaphore信號量)##############################

def run(n, semaphore):
    semaphore.acquire()
    print("run the thread: %s" % n)
    time.sleep(1)
    semaphore.release()

def test_run():
    semaphore = threading.BoundedSemaphore(5)
    # 这种锁允许一定数量的线程同时更改数据，它不是互斥锁。
    # 比如地铁安检，排队人很多，工作人员只允许一定数量的人进入安检区，
    # 其它的人继续排队。
    for i in range(20):
        t = threading.Thread(target=run, args=(i, semaphore))
        t.start()

##############################鎖(event)##############################
def event_func(e, i):
    print(i)
    # 檢測當前event是什麼狀態，如果是紅燈則阻塞，否則繼續往下執行，默認為紅燈
    e.wait()
    print(i + 100)

def test_event_func():
    event = threading.Event()
    for i in range(10):
        t = threading.Thread(target=event_func, args=(event, i))
        t.start()
    event.clear() # 主動將狀態設置為紅燈
    inp = input(">>>")
    if inp == "1":
        event.set() # 主動將狀態設置為綠燈

##############################鎖(condition)##############################
def condition():
    '''
    該機制會使的線程等待，只有滿足某條件時，才釋放n個線程
    '''
    ret = False
    r = input(">>>")
    if r == "yes" or r == "y":
        ret = True
    return ret

def condition_func(conn, i):
    print(i)
    conn.acquire()
    conn.wait_for(condition) # 這個方法接受一個函數的返回值
    print(i + 100)
    conn.release()

def test_conditon_func():
    c = threading.Condition()
    for i in range(10):
        t = threading.Thread(target=condition_func, args=(c, i))
        t.start()

##############################全局解釋鎖(gil)##############################
# 建议在IO密集型任务中使用多线程，在计算密集型任务中使用多进程。
# 深入研究python的协程机制，你会有惊喜的。

##############################Queue##############################
import queue
def queue_func():
    '''
    join() 阻塞进程，直到所有任务完成，需要配合另一个方法task_done。
    task_done() 表示某个任务完成。每一条get语句后需要一条task_done。
    '''
    q = queue.Queue(5)
    q.put(11)
    q.put(22)

    print(q.get())
    q.task_done()
    print(q.get())
    q.task_done()
    q.join()

def test_queue_func():
    queue_func()

##############################Thread pool##############################
class MyThreadPool:
    def __init__(self, maxsize=5):
        self.maxsize = maxsize
        self._q = queue.Queue(maxsize)
        for i in range(maxsize):
            self._q.put(threading.Thread)
    
    def get_thread(self):
        return self._q.get()

    def add_thread(self):
        self._q.put(threading.Thread)

def task(i, pool):
    print(i)
    time.sleep(1)
    pool.add_thread()

def test_thread_pool():
    pool = MyThreadPool()
    for i in range(100):
        t = pool.get_thread()
        obj = t(target=task, args=(i,pool))
        obj.start()

if __name__ == "__main__":
    test_show()

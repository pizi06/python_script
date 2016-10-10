# -*- coding:utf8 -*-

from multiprocessing import Process
import time
import random

####################################base#######################################
def base(i):
    print("This is Process ", i)

def test_base():
    for i in range(5):
        p = Process(target=foo, args=(i,))
        p.start()

####################################data#######################################
# 每个进程都有自己独立的数据空间，不同进程之间通常是不能共享数据，
# 创建一个进程需要非常大的开销。
list_1 = []
def data(i):
    list_1.append(i)
    print("This is Process ", i, " and list_1 is ", list_1)

def test_data():
    for i in range(5):
        p = Process(target=data, args=(i,))
        p.start()
    print("The end of list_1: ", list_1)

#################################share data####################################
# 使用Array共享数据
from multiprocessing import Array
def share_data_by_array(i, temp):
    temp[0] += 100
    for item in temp:
        print(i, "----->", item)

def test_share_data_by_array():
    # “i”表示它内部的元素全部是int类型，而不是指字符i，
    # 列表内的元素可以预先指定，也可以指定列表长度
    '''
    Array类在实例化的时候就必须指定数组的数据类型和数组的大小，
    类似temp = Array('i', 5)。对于数据类型有下面的表格对应：

    ‘c’: ctypes.c_char, ‘u’: ctypes.c_wchar,
    ‘b’: ctypes.c_byte, ‘B’: ctypes.c_ubyte,
    ‘h’: ctypes.c_short, ‘H’: ctypes.c_ushort,
    ‘i’: ctypes.c_int, ‘I’: ctypes.c_uint,
    ‘l’: ctypes.c_long, ‘L’: ctypes.c_ulong,
    ‘f’: ctypes.c_float, ‘d’: ctypes.c_double
    '''
    # temp = Array("i", [11, 22, 33, 44])
    temp = Array("i", 4)
    for i in range(2):
        p = Process(target=share_data_by_array, args=(i, temp))
        p.start()

# 使用Manager共享数据
from multiprocessing import Manager
def share_data_by_manager(i, dic):
    dic[i] = 100 + i
    print(dic.values())

def test_share_data_by_manager():
    manage = Manager()
    dic = manage.dict()
    for i in range(10):
        p = Process(target=share_data_by_manager, args=(i, dic))
        p.start()
        # TODO 沒有join會報錯，待研究
        p.join()

# 使用queue的Queue累共享數據
import multiprocessing
from multiprocessing import queues
# 数据共享中存在的脏数据,
# 比较悲催的是multiprocessing里还有一个Queue，一样能实现这个功能
def share_data_by_queue(i, arg):
    arg.put(i)
    print("The Process is ", i, " and the queue's size is ", arg.qsize())

def test_share_data_by_queue():
    li = queues.Queue(20, ctx=multiprocessing)
    for i in range(10):
        p = Process(target=share_data_by_queue, args=(i, li, ))
        p.start()

#################################process pool###################################
from multiprocessing import Pool
def process_pool(args):
    time.sleep(1)
    print(args)

def test_process_test():
    '''
    主要方法：
        apply：从进程池里取一个进程并执行
        apply_async：apply的异步版本
        terminate:立刻关闭进程池
        join：主进程等待所有子进程执行完毕。必须在close或terminate之后。
        close：等待所有进程结束后，才关闭进程池。
    '''
    p = Pool(5)
    for i in range(30):
        p.apply_async(func=process_pool, args=(i,))
    p.close() # 等子進程執行完畢后關閉進程池1
    # time.sleep(2)
    # p.terminate() # 立刻關閉進程池
    p.join()

#################################gevent########################################
from gevent import monkey; monkey.patch_all()
import gevent
import requests

def gevent_f(url):
    print("GET: %s" % url)
    resp = requests.get(url)
    data = resp.text
    print("%d bytes received from %s." % (len(data), url))

def test_gevent_f():
    gevent.joinall([
            gevent.spawn(gevent_f, "https://www.python.org/"),
            gevent.spawn(gevent_f, "https://www.baidu.com/"),
            gevent.spawn(gevent_f, "https://github.com/"),
    ])

if __name__ == "__main__":
    test_gevent_f()



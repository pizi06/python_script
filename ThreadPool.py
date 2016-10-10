# -*- coding:utf8 -*-

'''
一個機遇thread和queue的線程池，以任務為隊列元素，動態創建線程，重複利用線程，
通過close和terminate方法關閉線程池。
'''

import queue
import threading
import contextlib
import time

# 創建空對象，用於停止線程
StopEvent = object()

def callback(status, result):
    '''
    根據需要進行的回調函數，默認不執行。
    :param status: action函數的執行狀態
    :param result: action函數的返回值
    :return:
    '''
    pass

def action(thread_name, arg):
    '''
    真實的任務定義在這個函數里
    :param thread_name: 執行該方法的線程名
    :param arg: 該函數需要的參數
    '''
    # 模擬該函數執行了0.1秒
    time.sleep(0.1)
    print("第%s個任務調用了線程 %s，并打印了這條信息！" % (arg+1, thread_name))

class ThreadPool:
    def __init__(self, max_num, max_task_num=None):
        '''
        初始化線程池
        :param max_num: 線程池最大線程數量
        :param max_task_num: 任務隊列長度
        '''
        # 如果提供了最大任務數的參數，則將隊列的最大元素個數設置為這個值
        if max_task_num:
            self.q = queue.Queue(max_task_num)
        # 默認隊列可接受無限多個的任務
        else:
            self.q = queue.Queue()
        # 設置線程池最多可實例化的線程數
        self.max_num = max_num
        # 任務取消標識
        self.cancel = False
        # 任務中斷標識
        self.terminate = False
        # 已實例化的線程列表
        self.generate_list = []
        # 處於空閒狀態的線程列表
        self.free_list = []

    def put(self, func, args, callback=None):
        '''
        往任務列表里放入一個任務
        :param func: 任務函數
        :param args: 任務函數所需參數
        :param callback: 任務執行失敗或者成功后執行的回調函數，回調函數有兩個參數
        1，任務函數執行狀態；2，任務函數返回值（默認None，即：不執行回調函數）
        :return: 如果線程池已經終止，則返回True否則None
        '''
        # 先判斷標識，看看任務是否取消了
        if self.cancel:
            return
        # 如果沒有空閒的線程，並且已創建的線程的數量小於預定義的最大線程數，
        # 則創建新線程
        if len(self.free_list) == 0 and len(self.generate_list) > self.max_num:
            self.generate_thread()
        # 構造任務參數元組，分別調用的函數，該函數的參數，回調函數
        w = (func, args, callback)
        # 將任務放入列表
        self.q.put(w)

    def generate_thread(self):
        '''
        創建一個線程
        '''
        # 每個線程都執行call方法
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        '''
        循環去獲取任務函數并執行任務函數，在正常情況下，每個線程都保存生存狀態，
        直到獲取線程終止的flag。
        '''
        # 獲取當前線程的名字
        current_thread = threading.currentThread().getName()
        # 將當前線程的名字加入已實例化的線程列表中
        self.generate_list.append(current_thread)
        # 從任務列表中獲取一個任務
        event = self.q.get()
        # 讓獲取的任務不是終止線程的標識對象時
        while event != StopEvent:
            # 解析任務中封裝的三個參數
            func, arguments, callback = event
            # 抓取異常，放置線程因為異常退出
            try:
                # 正常執行任務函數
                result = func(current_thread, *arguments)
                success = True
            except Exception as e:
                # 當任務執行過程中彈出異常
                result = None
                success = False
            # 如果有指定的回調函數
            if callback is not None:
                # 執行回調函數，并抓取異常
                try:
                    callback(success, result)
                except Exception as e:
                    pass
            # 當某個線程正常執行完一個任務時，先執行worker_state方法
            with self.worker_state(self.free_list, current_thread):
                # 如果強制關閉線程的flag開啟，則傳入一個StopEvent元素
                if self.terminate:
                    event = StopEvent
                # 否則獲取一個正常的任務，并回調worker_state方法的yield語句
                else:
                    # 從這裡開始又一個正常的任務循環
                    event = self.q.get()
        else:
            # 一旦發現任務時個終止線程的標識元素，將線程從已創建線程列表中刪除
            self.generate_list.remove(current_thread)
    def close(self):
        '''
        執行完所有的任務后，讓所有線程都停止方法
        '''
        # 設置flag
        self.cancel = True
        # 計算已創建線程列表中線程的個數，
        # 然後往任務隊列裡推送相同數量的終止線程的標識元素
        full_size = len(self.generate_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1

    def terminate(self):
        '''
        在任務執行過程中，終止線程，提前退出
        '''
        self.terminate = True
        # 強制性的停止線程
        while self.generate_list:
            self.q.put(StopEvent)

    # 該裝飾器用於上下文管理
    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        '''
        用於記錄空閒的線程，或沖空閒列表中取出線程處理任務
        '''
        # 將當前線程，添加到空閒線程列表中
        state_list.append(worker_thread)
        # 捕獲異常
        try:
            # 在此等待
            yield
        finally:
            # 將線程從空閒列表中移除
            state_list.remove(worker_thread)

# 調用方式
if __name__ == "__main__":
    # 創建一個最多包含5個線程的線程池
    pool = ThreadPool(5)
    # 創建100個任務，讓線程池進行處理
    for i in range(100):
        pool.put(action, (i,), callback)
    # 等待一定時間，讓線程執行任務
    time.sleep(3)
    print("-" * 50)
    print("33[32;0m任務終止前線程池中有%s個線程，空閒的線程有%s個！33[0m"
            % (len(pool.generate_list), len(pool.free_list)))
    # 正常關閉線程池
    pool.close()
    print("任務執行完畢，正常退出")
    # 強制關閉線程池
    #pool.terminate()
    #print("強制停止任務")




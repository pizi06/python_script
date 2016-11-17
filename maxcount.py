if __name__ == "__main__":
    
    ''' 获取列表里重复元素最多的重复数，对collections.Counter和list.count的对比。
    list.count胜出
    '''
    import time
    import random
    from collections import Counter
    a =  random.sample(range(10)*10, 4)
    count = 10000
    st = time.time()
    for i in range(count):
        b = max(Counter(a).values())
    print "Counter cost: ", time.time() - st
    #Counter cost:  0.0840229988098
    st = time.time()
    for i in range(count):
        a.count(max(a, key=a.count))
    print "count cost:", time.time() - s
    # count cost: 0.0126390457153

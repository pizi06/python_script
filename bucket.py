# -*- coding:utf8 -*-
import time
import random

#a = [1,2,3,2,1,2,3,4,6,7,8,11,13]
def bucket(a):
    b = [0] * 15
    # print b

    for i in a:
        b[i-1] = 1
        
    #print "=" * 80
    #print b

    temp = 0
    shunzilen = 0
    for i in b:
        if i == 1:
            temp += 1
        else:
            if shunzilen < temp:
                shunzilen = temp
            temp = 0
    shunzilen = shunzilen if shunzilen > 1 else 0
    #print "shunzilen: ", shunzilen
    
def normal(a):
    b = sorted(list(set(a)))
    #print "b: ", b
    temp =  0
    shunzilen = 0
    for i, v in enumerate(b):
        if i == 0:
            temp = 1
            continue
        elif v == b[i-1] + 1:
            temp += 1
        else:
            if shunzilen < temp:
                shunzilen = temp
            temp = 0
    shunzilen = shunzilen if shunzilen > 1 else 0
    #print "normal: ", shunzilen

if __name__ == "__main__":
    count = 10000
    
    s_t = time.time()
    a = [random.randint(1,15) for i in xrange(20)]
    print a
    for i in xrange(count):
        normal(a)
    print "normal cost time: ", time.time() - s_t
    s_t = time.time()
    for i in xrange(count):
        bucket(a)
    print "bucket cost time: ", time.time() -  s_t
# -*- coding:utf8 -*-

# http://www.pythonchallenge.com/pc/def/map.html

import string
from string import ascii_lowercase


def transfer(s):
    """
    自己写的，翻译完他的句子才发现推荐使用string.maketrans，真的快好多啊
    """
    r = ""
    for i in s:
        if i in ascii_lowercase:
            get_index = ascii_lowercase.index(i)-len(ascii_lowercase) + 2
            r += ascii_lowercase[get_index]
        else:
            r += i
    return r


def test_cost_time():
    """
    maketrans end cost:  0.18799996376
    transfer end cost:  12.628000021
    """
    import time
    count = 100000
    start_time = time.time()
    for i in xrange(count):
        trans = string.maketrans(ascii_lowercase, ascii_lowercase[2:] + ascii_lowercase[:2])
        r = s.translate(trans)
    print "maketrans end cost: ", time.time() - start_time
    
    start_time = time.time()
    for i in xrange(count):
        transfer(s)
    print "transfer end cost: ", time.time() - start_time
    
if __name__ == "__main__":
    """
    i hope you didnt translate it by hand. thats what computers are for.
    doing it in by hand is inefficient and that's why this text is so long.
    using string.maketrans() is recommended. now apply on the url.
    """
    s = """
        g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp.
        bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle.
        sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.
    """
    s = 'map'
    trans = string.maketrans(ascii_lowercase, ascii_lowercase[2:] + ascii_lowercase[:2])
    r = s.translate(trans)
    print r


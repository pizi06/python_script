# -*- coding:utf-8 -*-
'''
Created On 2017年02月06日

@author: yinpilei
'''

# Python3
def to_str(bytes_or_str):
    ''' 接受str或者bytes，并总是返回str
    '''
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value


def to_bytes(bytes_or_str):
    ''' 接受str或bytes，并总是返回bytes
    '''
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value


# Python2
def py2_to_unicode(unicode_or_str):
    ''' 接受str或unicode，并总是返回unicode
    '''
    if isinstance(unicode_or_str, str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str
    return value


def py2_to_str(unicode_or_str):
    ''' 接受str或unicode，并总是返回str
    '''
    if isinstance(unicode_or_str, unicode):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value


# -*- coding:utf8 -*-

import os, sys
# 本想用正則表達是來獲取同一類型的文件，后一想現在只是為了找到pyc文件，
# 就直接用[-3:]，不用那麼複雜
# import re

# 翻了一下os的文檔，知道看到remove沒看到move，上網找打shutil可以move
import shutil
import time

base_path = "D:\git\gfirefly_study\gfirefly_study"
base_dir = "D:\git\gfirefly_study\gfirefly_study"

def get_files(base_path):
    files = os.listdir(base_path)
    for f in files:
        # 最初語法高亮顯得少了個引號，就直接多加了個引號，但跑出來，
        # 卻一直沒有東西，才反應過來，斜杠要轉譯而不是引號要轉譯
        # full_path = base_path + "\"" + f
        full_path = base_path + '\\' + f
        if os.path.isdir(full_path):
            get_files(full_path)
        else:
            if f[-3:] == "pyc":
                try:
                    os.rename(full_path, base_dir+f)
                    #shutil.move，因为它是基于复制的，同盘的移动文件  
                    #效率很低，而os.rename对于同盘文件的移动相当快  
                    #其实它就是更改了一下文件属性  
                    # shutil.move(full_path, base_dir)
                except:
                    #  win下的坑，文件後綴不能太長。（4）
                    # os.rename(full_path, base_path + f + str(time.time))
                    os.rename(full_path, base_path + str(time.time()) + f)


if __name__ == "__main__":
    get_files(base_path)

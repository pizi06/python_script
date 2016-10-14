# -*- coding:utf8 -*-

# http://www.pythonchallenge.com/pc/def/channel.html
# 图片为一个拉链，考验英语的时候啊，zip为拉链
# 访问http://www.pythonchallenge.com/pc/def/channel.zip
# 下载到一个zip文件，解压后有个readme.txt文件，告知得从90052开始
# 到最后一个文件告知查看comment，上网查找zipfile库的使用方法。
# http://python.jobbole.com/81519/
# zf = zipfile.ZipFile(zip_file_name)
# zipinfo = zf.getinfo(file_name)表示zip文档中相应file_name文件的信息
# zipinfo.comment 文档说明

import os
import re
import zipfile

def foo():
    zip_file = zipfile.ZipFile("channel.zip")
    base_path = "./channel"
    l = os.listdir(base_path)

    nothing =  "90052"
    comments = ""
    while nothing:
        file_name = os.path.join(base_path, nothing + ".txt")
        with open(file_name) as f:
            text = "".join(f.readlines())
            #print "file_name:", file_name, " context: ", text
            try:
                comments += zip_file.getinfo(nothing + ".txt").comment
                nothing = re.findall(r"\d+", text)[-1]
            except Exception, e:
                print "error: ", e, " text: ", text
                nothing = ""
    print comments
    # the last file_name: ./channel\46145.txt  context:  Collect the comments.

if __name__ == "__main__":
    foo()
    # result: hockey
    '''
****************************************************************
****************************************************************
**                                                            **
**   OO    OO    XX      YYYY    GG    GG  EEEEEE NN      NN  **
**   OO    OO  XXXXXX   YYYYYY   GG   GG   EEEEEE  NN    NN   **
**   OO    OO XXX  XXX YYY   YY  GG GG     EE       NN  NN    **
**   OOOOOOOO XX    XX YY        GGG       EEEEE     NNNN     **
**   OOOOOOOO XX    XX YY        GGG       EEEEE      NN      **
**   OO    OO XXX  XXX YYY   YY  GG GG     EE         NN      **
**   OO    OO  XXXXXX   YYYYYY   GG   GG   EEEEEE     NN      **
**   OO    OO    XX      YYYY    GG    GG  EEEEEE     NN      **
**                                                            **
****************************************************************
 **************************************************************
    '''
    # 以为是hockey，浏览http://www.pythonchallenge.com/pc/def/oxygen.html
    # 提示：it's in the air. look at the letters.
    # 只能求助google了，才知道是oxygen。
    # h是用多个o组成，o是用x，c是y，k是g，e是e，y是n

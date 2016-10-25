# -*- coding:utf8 -*-

import requests
import re
#import Image

# http://www.pythonchallenge.com/pc/def/oxygen.html
# 出现一张带马赛克的图片，估计和图片相关的库有关了。
# image_url = "http://www.pythonchallenge.com/pc/def/oxygen.png"
# 下载下来，保存为oxygen.png
# im = Image.open("oxygen.png")
# print help(im.getpixel)
# print im.getpixel((1,1))
# print chr(im.getpixel((3, 43))[0])
# IOError: decoder zip not available
# 上网搜到，有人建议用pillow pip安装试一试
# 用gimp把类似马赛克的图片截出来

from PIL import Image
im = Image.open("oxygen_cut.png")
# print im.mode, im.getpixel((1,1)),dir(im)

#print im.getdata(), im.size
# <ImagingCore object at 0x0000000002A0CB10> (609, 11)

#print "".join([chr(im.getpixel((i, 3))[0]) for i in xrange(609)])
'''
sssssmmmmmmmaaaaaaarrrrrrrttttttt       ggggggguuuuuuuyyyyyyy,,,,,,,       yyyyy
yyooooooouuuuuuu       mmmmmmmaaaaaaadddddddeeeeeee       iiiiiiittttttt.......
      ttttttthhhhhhheeeeeee       nnnnnnneeeeeeexxxxxxxttttttt       llllllleeee
eeevvvvvvveeeeeeelllllll       iiiiiiisssssss       [[[[[[[111111100000005555555
,,,,,,,       111111111111110000000,,,,,,,       111111111111116666666,,,,,,,
    111111100000001111111,,,,,,,       111111100000003333333,,,,,,,       111111
111111114444444,,,,,,,       111111100000005555555,,,,,,,       1111111111111166
66666,,,,,,,       111111122222221111111]]]]]]]]{
'''
# 细数了一下都是7个7个一组，前面的5个s估计是截图的时候少截了，但不妨碍步长7
context = "".join([chr(im.getpixel((i, 3))[0]) for i in xrange(0, 609, 7)])
# print context
# smart guy, you made it. the next level is 
# [105, 110, 116, 101, 103, 114, 105, 116, 121]
real_context = [105, 110, 116, 101, 103, 114, 105, 116, 121]
result = ''
for i in real_context:
    result += chr(i)
print result

# 顺便再用一下正则表达式
print ''.join([chr(int(x)) for x in re.findall(r'\d{3}', context)])

# -*- coding:utf8 -*-

import requests

# http://www.pythonchallenge.com/pc/def/oxygen.html
url = "http://www.pythonchallenge.com/pc/def/oxygen.html"
r = requests.get(url)
print r.text
# 出现一张带马赛克的图片，估计和图片相关的库有关了。

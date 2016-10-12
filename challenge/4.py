# -*- coding:utf8 -*-

import requests
import re

# http://www.pythonchallenge.com/pc/def/linkedlist.php
# title: follow the chain

if __name__ == "__main__":
    # http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=12345
    # and the next nothing is 44827
    # and the next nothing is 45439
    # Your hands are getting tired and the next nothing is 94485 72198
    # nothing = "12345"
    # Yes. Divide by two and keep going.
    nothing = "8022"
    # text. One example is 82683. Look only for the next nothing and the next
    # nothing is 63579
    nothing = "63579"
    url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
    while nothing:
        r = requests.get(url + nothing)
        text = r.text
        print "text: ", text
        nothing = re.findall(r"\d+", text)[-1]
        print nothing
    print "finally: ", text
    # result: peak.html




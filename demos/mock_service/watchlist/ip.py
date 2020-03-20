#!/usr/bin/env python3
# @Time    : 2020-3-20 18:24
# @Author  : chen
# @FileName: ip.py
# @Software: PyCharm

import socket

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    ip = s.getsockname()[0]
finally:
    s.close()
print(ip)

url = "http://%s:%s" % (ip, 5001)
print(url)
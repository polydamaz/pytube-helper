#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

print(os.path.abspath(os.path.curdir), "\n", os.path.curdir)


sys.exit()


rt = []

def gul():
    testDic = [
        {'one':'1', 'two':'2', 'three':'3'},
        {'one':'2', 'two':'3', 'three':'4'},
        {'one':'3', 'two':'4', 'three':'5'}
    ]
    for n in testDic:
        if 'one' in n and n['one'] == '1':
            rt.append(n)
gul()
print(rt)
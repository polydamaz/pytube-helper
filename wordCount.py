# -*- coding: utf-8 -*-
"""
완성 (단어 수 & 내림차순)
다음 목표: 텍스트 파일을 읽어 [줄 수, 글자 수] 알아내기
"""
import operator

def wordCount(paragraph):
    countList = {}
    for word in paragraph.split():
        word = word.lower()
        if word not in countList:
            countList[word] = 1
        else:
            countList[word] += 1
    return countList

txt = 'Better Selection of Software Providers Through Trialsourcing Failure Factors of Software Projects at a Global Outsourcing Marketplace When is a low bid price a thread and when an opportunity for your project? Analyzing projects in an online marketplace for outsourcing software development A Strong Focus on Low Price When Selecting Software Providers Increases the Likelihood of Failure in Software Outsourcing Projects. Too Nothing Better'
sam = wordCount(txt)

for i in sorted(sam.items(), key=operator.itemgetter(1), reverse=True): 
    print(i)
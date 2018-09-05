#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, html
from urllib.request import Request, urlopen
from pytube import YouTube

import sys

__version__ = '0.3.2'
"""
class 최소화 

1. 깜빡임 문제
2. 단일 다운로드 시 제목 안뜸
3. 자소 분리
처리 후 최대한 
"""


    # @property
    # def status(self):
    #     if self.__cur == 0:
    #         return self.__status[0]
    #     elif self.__cur == 100:
    #         return self.__status[2]
    #     else:
    #         return self.__status[1]
    
    # def perc(self, cur=0, filesize=0):
    #     if filesize == 0 or cur == 0:
    #         pass
    #     else:
    #         # per = (self.filesize - cur / self.filesize)
    #         per = (cur / filesize)
    #         self.__cur = 100 if per >= 1 else int(per * 100)

    #     self.__filesize = filesize
    #     return self.__cur
class Listitem():
    def __init__(self, **attributes):
        self.title = ''
        self.vid = ''
        self.code = ''
        self.url = ''
        self.cur = 0
        self.status = '0'
        self.totalDn = ''
        self.confirmDn = False
        self.item = None

        if attributes is not None:
            self.__setProperty(attributes.items())
            
    def __setProperty(self, attribute):
        for key, val in attribute:
                try:
                    self.__getattribute__(key)
                    self.__setattr__(key, val)
                except AttributeError:
                    continue



class Playlist():
    def __init__(self, url=None, downloadPath=None):
        self.__youtubeURL = url
        self.__url = self.__getURL()
        self.__title = ''
        self.__downloadPath = './' if downloadPath is '.' else downloadPath
        self.__items = []
        self.__downloadList = []
        self.__ListItems = []
        self.__totSum = 0
        self.downloadStart = False
        self.selfTimer = 0

        if self.__url:
            self.__extractItem()
        else:
            # self.__items.append({
            #     'siz': 0, 'per': 0, 'url': self.__youtubeURL,
            #     'code': '(1)', 'title':''
            # })
            self.__items.append(Listitem(url=self.__youtubeURL, code='00'))

    @property
    def listTitle(self):
        return self.__title
    
    @property
    def items(self):
        return self.__items
    
    
    @property
    def downloadPath(self):
        return self.__downloadPath
 
    @property
    def url(self):
        return self.__url

    def setItem(self, no, key, val):
        self.__items[no][key] = val

    def perc(self):
        numOfDnItems = 0
        totSum = 0 
        for i in self.__items:
            if i.confirmDn:
                totSum += i.cur
                numOfDnItems += 1
        
        if totSum == 0 or numOfDnItems == 0:
            # return 0, 0
            return 0
        else:
            return (totSum / (numOfDnItems * 100)) * 100
            # return (numOfDnItems, totSum)

    def downloadConfirm(self, i, confirmDn=False, **kwargs):
        if self.__items[i].confirmDn:
            self.__items[i].item = YouTube(self.__items[i].url, on_progress_callback=kwargs['on_progress_callback'])
            self.__items[i].vid = self.__items[i].item.player_config_args['video_id']
            self.__items[i].item.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(self.__downloadPath)

    def download(
        self, url, code=0, 
        defer_prefetch_init=None, on_complete_callback=None, on_progress_callback=None, proxies=None
    ):
        self.__ListItems.append(
            # ListItem(url, code, defer_prefetch_init, on_complete_callback, on_progress_callback, proxies)
            YouTube(url, defer_prefetch_init, on_progress_callback, on_complete_callback, proxies)
        )
        # self.__ListItems[-1].streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(self.__downloadPath)
        self.__ListItems[-1].streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(self.__downloadPath)
        # self.__ListItems[-1].streams.filter(progressive=True, file_extension='mp4')
        # self.__ListItems[-1].order_by('resolution')
        # self.__ListItems[-1].desc().first().download(self.__downloadPath)
        # # self.__ListItems[len(self.__ListItems) -1].streams.set_attributes_from_dict(('code',code))
        return self.__ListItems
        
    def downloadCheckTags(self, tags=()):
        for n in self.__items:
            if n.code in tags:
                # self.__downloadList.append(n)
                n.confirmDn = True

        # return self.__downloadList
    
    def __getURL(self):
        qstr = self.__youtubeURL[self.__youtubeURL.find('?')+1:]
        for el in qstr.split('&'):
            if 'list' in el.split('='):
                return 'https://www.youtube.com/playlist?{}'.format(el)
        return None

    def __stripTag(self, string):
        rx = re.compile('([&#~*=+?:;|<>,/\'\"])')
        return (rx.sub('', html.unescape(string))).strip()

    def __extractItem(self):
        titleLine = False
        request = Request(self.__url)
        tempList = []
        n = 0

        for line in urlopen(request).readlines():
            tag = line.decode('utf8')
            if '<title>' in tag:
                self.__title = self.__stripTag( tag.split('<title>',1)[1].split(' - YouTube</title>',1)[0])

            if titleLine :
                tempList[-1].title += tag.strip()
                titleLine = False

            if 'pl-video-title-link' in tag:
                tempList.append(Listitem(
                    url = 'https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0],
                    code = str(n).zfill(2)
                ))
                titleLine = True
                n += 1

        self.__items = tempList
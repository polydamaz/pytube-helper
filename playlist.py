#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, html
from urllib.request import Request, urlopen
from pytube import YouTube

__version__ = '0.3.2'

class Listitem():
    def __init__(self, **attributes):
        self.__title = ''
        self.vid = ''
        self.code = ''
        self.url = ''
        self.cur = 0
        self.state = 'Wait'
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

    @property
    def title(self):
        if self.item:
            return self.item.title
        else:
            return self.__title

    @title.setter
    def title(self, text):
        self.__title = text
        if self.item:
            self.item.title = text

    

class Playlist():
    def __init__(self, url=None, downloadPath=None):
        self.__youtubeURL = url if url else 'https://www.youtube.com/watch?v=-VRfO2hlf54&list=PLuHgQVnccGMBe0848t2_ZUgFNJdanOA_I' # test url
        self.__url = self.__getURL()
        self.__title = ''
        self.__downloadPath = './' if downloadPath is '.' else downloadPath
        self.__items = []

        if self.__url:
            self.__extractItem()
        else:
            self.__items.append(Listitem(url=self.__youtubeURL, code='00'))
            self.__items[0].item = YouTube(self.__youtubeURL)

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

    def perc(self):
        numOfDnItems = 0
        totSum = 0 
        for i in self.__items:
            if i.confirmDn:
                totSum += i.cur
                numOfDnItems += 1
        
        if totSum == 0 or numOfDnItems == 0:
            return 0
        else:
            return (totSum / (numOfDnItems * 100)) * 100

    def download(self, i=0, **kwargs):
        if self.__items[i].confirmDn:
            if self.__items[i].item == None: 
                self.__items[i].item = YouTube(self.__items[i].url, on_progress_callback=kwargs['on_progress_callback'])
            else:
                if kwargs['on_progress_callback']:
                    self.__items[i].item.register_on_progress_callback(kwargs['on_progress_callback'])

            self.__items[i].vid = self.__items[i].item.player_config_args['video_id']
            self.__items[i].item.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(self.__downloadPath)

    def checkDownload(self, tags=()):
        for n in self.__items:
            if n.code in tags:
                n.confirmDn = True
    
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
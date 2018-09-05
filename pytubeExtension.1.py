#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, html
from urllib.request import Request, urlopen
from pytube import YouTube, Stream, StreamQuery
# from pytube.helpers import safe_filename

__version__ = '0.3.2'

class StreamList(Stream):
    def __init__(self, stream, player_config_args, monostate, itemInfo=None):
        # super().__init__(stream, player_config_args, monostate)
        self.itemInfo = itemInfo

class ListItem(YouTube):
    def __init__(
        self, url=None, code=0, 
        defer_prefetch_init=False, on_progress_callback=None, on_complete_callback=None, proxies=None
    ):
        self.__status = ('Wait', 'Downloading', 'Complete')
        self.__cur = 0
        self.__code = code
        self.__filesize = 0

        # self.member = 0
        # self.fmt_streams = []
        # super().__init__(url, defer_prefetch_init, on_progress_callback, on_complete_callback, proxies)
    
    @property
    def code(self):
        return self.__code
    
    @property
    def cur(self):
        return self.__cur

    def initialize_stream_objects(self, fmt):
        stream_manifest = self.player_config_args[fmt]
        for stream in stream_manifest:
            video = StreamList(
                stream=stream,
                player_config_args=self.player_config_args,
                monostate=self.stream_monostate,
                itemInfo={
                    'title':self.title,
                    'code':self.__code,
                    'cur':self.__cur
                }
            )
            self.fmt_streams.append(video)
        
    
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

        if self.__url:
            self.__extractItem()
        else:
            self.__items.append({
                'siz': 0, 'per': 0, 'url': self.__youtubeURL,
                'code': '(1)', 'title':''
            })

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
    
    def perc(self, cur):
        self.__totSum += cur
        if self.__totSum or cur == 0:
            return 0
        else:
            return (((len(self.__downloadList) * 100) + self.__totSum) / self.__totSum) * 100

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
            if n['code'] in tags:
                self.__downloadList.append(n)

        return self.__downloadList
    
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
                # self.__title = safe_filename( tag.split('<title>',1)[1].split(' - YouTube</title>',1)[0])

            if titleLine :
                tempList[len(tempList)-1]['title'] += tag.strip()
                titleLine = False

            if 'pl-video-title-link' in tag:
                item = {
                    'siz': 0,
                    'per': 'wait',
                    'url': 'https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0],
                    'code': '({})'.format(n),
                    'title': ''
                }
                tempList.append(item)
                titleLine = True
                n += 1

        self.__items = tempList
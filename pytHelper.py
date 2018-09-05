#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time
import argparse
import re
import locale
import html

from dialog import Dialog
from urllib.request import Request, urlopen
from pytube import YouTube

__version__ = '0.3.1'

class PytHelper(YouTube):
    def __init__(
        self, url=None, downloadPath=None, 
        defer_prefetch_init=False, on_progress_callback=None, on_complete_callback=None, proxies=None
    ):
        YouTube.__init__(
            self, url=url, defer_prefetch_init=defer_prefetch_init, 
            on_progress_callback=on_progress_callback, on_complete_callback=on_complete_callback, proxies=proxies
        )
        
        self.__url = url
        self.__playListURL = self.__getPlayListURL()
        self.__playListTitle = ''
        self.__downloadPath = './' if downloadPath is '.' else downloadPath
        self.__playList = []

        if self.__playListURL:
            self.__extractPlayList()
        else:
            self.__playList.append({
                'siz': 0, 'per': 0, 'url': self.__url,
                'code': '(1)', 'title': self.__stripTag(self.title)
            })

    @property
    def playListTitle(self):
        return self.__playListTitle
    
    @property
    def playList(self):
        return self.__playList

    @property
    def downloadPath(self):
        return self.__downloadPath
 
    @property
    def playListURL(self):
        return self.__playListURL
 
    def __getPlayListURL(self):
        qstr = self.__url[self.__url.find('?')+1:]
        for el in qstr.split('&'):
            if 'list' in el.split('='):
                return 'https://www.youtube.com/playlist?{}'.format(el)
        return None

    def __stripTag(self, string):
        rx = re.compile('([&#~*=+?:;|<>,/\'\"])')
        return (rx.sub('', html.unescape(string))).strip()

    def __extractPlayList(self):
        titleLine = False
        request = Request(self.__playListURL)
        playList = []
        n = 0

        for line in urlopen(request).readlines():
            tag = line.decode('utf8')
            if '<title>' in tag:
                self.__playListTitle = self.__stripTag( tag.split('<title>',1)[1].split(' - YouTube</title>',1)[0])
            if titleLine :
                playList[len(playList)-1]['title'] += tag.strip()
                titleLine = False
            if 'pl-video-title-link' in tag:
                item = {
                    'siz': 0,
                    'per': 'wait',
                    'url': 'https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0],
                    'code': '({})'.format(n),
                    'title': ''
                }
                playList.append(item)
                titleLine = True
                n += 1

        self.__playList = playList 

if __name__ == "__main__" :
    
    def perc(cur, total):
        return int((cur / total) * 100)

    def progress_function(self, chunk, file_handle, bytes_remaining):
        if downloadList[nl]['siz'] is 0:
            downloadList[nl]['siz'] = self.filesize
            
        downloadList[nl]['per'] = int(perc(self.filesize - bytes_remaining, downloadList[nl]['siz']))
        dc['totPer'] = perc((nl * 100) + downloadList[nl]['per'], dc['totSum'])

        d.mixedgauge(
            text = '',
            elements = [(item['title'], '-' + str(item['per']) if type(item['per']) is int else item['per']  ) for item in downloadList],
            percent = dc['totPer'],
            title= pyt.playListTitle
        )

    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-p PLAYLISTURL] [-d DESTINATION]')
    parser.add_argument('-p', '--playlisturl', help='url of the playlist to be downloaded', default='', metavar='')
    parser.add_argument('-d', '--destination', help='path of directory to save videos to', default=os.path.curdir, metavar='')
    args = parser.parse_args()
    
    url = ''
    d = Dialog(dialog="dialog")
    d.set_background_title("Pytube List Dowload Helper {}".format(__version__))

    m01 = u"주소 입력"
    m02 = u"처리중입니다."
    if args.playlisturl is '':
        code, url = d.inputbox(text=m01,width=50)
        if code is d.CANCEL:
            sys.exit()
    else:
        d.infobox(text=m02)

    m03 = u"다운로드 받을 경로 입력."
    code, path = d.dselect(filepath=os.path.abspath(args.destination), width=50)
    if code == d.CANCEL:
        sys.exit()

    d.infobox(text=m02)
    pyt = PytHelper(url if url else args.playlisturl, path)
    playList = pyt.playList
    d.infobox(text=m02)

    m03 = u"다운받을 영상을 선택하세요."
    code, tags = d.checklist(m03, choices=[(item['code'], item['title'], True) for item in playList])

    downloadList = []

    for n in playList:
        if n['code'] in tags:
            downloadList.append(n)

    d.infobox(text=m02)

    if code == d.OK:
        nl = 0
        dc = {'totSum': 0, 'totPer': 0, 'totLen': len(downloadList)}

        for item in downloadList:
            dc['totSum'] = dc['totLen'] * 100
            yt = YouTube(item['url'], on_progress_callback=progress_function)
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(pyt.downloadPath)
            
            nl += 1

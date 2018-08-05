#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time
import argparse
import re
import locale
import html

from dialog import Dialog
from urllib.request import Request,urlopen
from pytube import YouTube

__version__ = '0.3.1'

class PytHelper(YouTube):
    """Sub Class"""
    def __init__(self, url, downloadDir, defer_prefetch_init=False):
        YouTube.__init__(self, url, defer_prefetch_init)
        
        self.url = url
        self.downloadDir = downloadDir
        self.playList = []
        self.playListURL = ''
        self.playListTitle = ''
        self.currentDownload = None
        self.totSum = 0
        self.totPerSum = 0
        self.totPer = 0

        self.main()

    def main(self):
        # list gubun
        self.playListURL = self.getList(self.url)
        # init path
        if self.downloadDir is '.':
            self.downloadDir += '/' 

        # has playList
        if self.playListURL:
            self.__extractPlayList()
        else: 
            self.playList.append({
                'siz': 0,
                'per': 0,
                'url': self.url,
                'code': '(1)',
                'title': '0 title'
            })

    def getPlayList(self):
        return self.playList
            
    def downPlaylist(self,dic=[]):
        for u in self.playList:
            if u['code'] in dic:
                yt = YouTube(u['url'])
                vid = yt.streams.filter(mime_type='video/mp4').order_by('resolution').last()
                if self.downloadDir is '.':
                   self.downloadDir += '/' 
                directory_contents = [f.split('.mp4',1)[0] for f in os.listdir(self.downloadDir) if f.endswith('.mp4')]
                # print('path={}{}'.format(self.downloadDir, vid.default_filename) )
                if vid.default_filename in directory_contents:
                    print('Skipping {}'.format(vid.default_filename))
                    continue
                else:
                    print('Downloading {}'.format(vid.default_filename))
                    vid.download(self.downloadDir) 
                    print('Done')     
            else:
                print('##')
        sys.exit()

    def downloadVideo(self, url, progress_function=None, complete_function=None):
        yt = YouTube(url, on_progress_callback=progress_function, on_complete_callback=complete_function)
        """ 여기서 확장자 선택"""
        vid = yt.streams.filter(mime_type='video/mp4').order_by('resolution').last()

        # directory_contents = [f.split('.mp4',1)[0] for f in os.listdir(self.downloadDir) if f.endswith('.mp4')]
        
        # if vid.default_filename in directory_contents:
        #     print('Skipping {}'.format(vid.default_filename))
        #     return False
        # self.currentDownload = vid
        vid.download(self.downloadDir)
             
    @staticmethod	
    def stripTag(string):
        rx = re.compile('([&#~*=+?:;<>,/\'\"])')
        return (rx.sub('', html.unescape(string))).strip()

    @staticmethod
    def getList(url):
        qstr = url[url.find('?')+1:]
        for el in qstr.split('&'):
            if 'list' in el.split('='):
                return 'https://www.youtube.com/playlist?{}'.format(el)
        
    def __extractPlayList(self):
        titleLine = False
        request = Request(self.playListURL)
        n = 0

        for line in urlopen(request).readlines():
            tag = line.decode('utf8')

            if '<title>' in tag:
                self.playListTitle = self.stripTag( tag.split('<title>',1)[1].split(' - YouTube</title>',1)[0])

            if titleLine :
                self.playList[len(self.playList)-1]['title'] += tag.strip()
                titleLine = False

            if 'pl-video-title-link' in tag:
                playList = {
                    'siz': 0,
                    'per': 'wait',
                    'url': 'https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0],
                    'code': '({})'.format(n),
                    'title': ''
                }
                self.playList.append(playList)
                titleLine = True
                n += 1
                # self.playList.append('https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0])

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
    playList = pyt.getPlayList()    

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
            vid = yt.streams.filter(mime_type='video/mp4').order_by('resolution').last()
            vid.download(pyt.downloadDir)
            nl += 1

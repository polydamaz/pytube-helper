# -*- coding: utf-8 -*-
import os, sys, time
import argparse
import re
import urllib

from pytube import YouTube

# reload(sys)
# sys.setdefaultencoding('utf-8')
# from urllib2 import urlopen


# =============================
# Utility functions and classes
# =============================
class PytHelper(YouTube):
    """Sub Class"""
    def __init__(self, url, downloadDir, defer_prefetch_init=False):
        YouTube.__init__(self, url, defer_prefetch_init)
        
        self.url = url
        self.downloadDir = downloadDir
        self.playList = []
        self.playListURL = ''
        self.playListTitle = ''
        
        self.main()

    def main(self):
        # list gubun
        self.playListURL = self.getList(self.url)

        # has playList
        if self.playListURL:
            self.__extractPlayList()
            sys.exit()
        else: 
            self.playList.append({
                'url':self.url,
                'title':''
            })

        if os.path.exists(self.downloadDir):
            directory_contents = [f.split('.mp4',1)[0] for f in os.listdir(self.downloadDir) if f.endswith('.mp4')]
        else:
            print('Destination directory does not exist')
            sys.exit(1)

        confirmation = raw_input("You are about to download {0} videos to {1}\nWould you like to continue? Y/n ".format(len(self.playList), os.path.abspath(self.downloadDir)))
        
        if confirmation.lower() in ['n']:
            print 'GoodBye'
            sys.exit()
        
        for u in self.playList:
            yt = YouTube(u['url'])
            vid = yt.streams.filter(mime_type='video/mp4').order_by('resolution').last()
            if vid.default_filename in directory_contents:
                print('Skipping {}'.format(vid.default_filename))
                continue
            else:
                print('Downloading {}'.format(vid.default_filename))
                vid.download(self.downloadDir) 
                print('Done')
        
    @staticmethod
    def makeFolder(dirname):
        try :
            os.makedirs(dirname)
        except OSError :
            print OSError.errno
            if os.path.exists(dirname):
                # We are nearly safe
                print OSError.errno+"folder exists"
                pass
            else:
                # There was an error on creation, so make sure we know about it
                print OSError.errno
                raise

    @staticmethod	
    def possibleName(str):
        rx = re.compile('([&#~*=+?:;<>,/])')
        return rx.sub('', str)
        
        
    @staticmethod
    def getList(url):
        qstr = url[url.find('?')+1:]
        for el in qstr.split('&'):
            if 'list' in el.split('='):
                return 'https://www.youtube.com/playlist?{}'.format(el)
        
    @staticmethod
    def extractPlayList(url):
        playList = []
        for line in urllib.urlopen(url).readlines():
            tag = line.decode('utf8')
            if 'pl-video-title-link' in tag:
                playList.append('https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0])
        return playList

    def __extractPlayList(self):
        titleLine = False
        for line in urllib.urlopen(self.playListURL).readlines():
            tag = line.decode('utf8')
            # tag = line
            if '<title>' in tag:
                self.playListTitle = tag.split('<title>',1)[1].split(' - YouTube</title>',1)[0]

            if titleLine :
                self.playList[len(self.playList)-1]['title'] = tag.strip()
                titleLine = False

            if 'pl-video-title-link' in tag:
                playList = {
                    'url': 'https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0],
                    'title': ''
                }
                self.playList.append(playList)
                titleLine = True
                # self.playList.append('https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0])


if __name__ == "__main__" :
    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-p PLAYLISTURL] [-d DESTINATION]')
    parser.add_argument('-p', '--playlisturl', help='url of the playlist to be downloaded', default='https://www.youtube.com/watch?v=kN6mlybyTdA&list=PLuHgQVnccGMDMxfZEpLbzHPZUEwObEaZq', metavar='')
    parser.add_argument('-d', '--destination', help='path of directory to save videos to', default=os.path.curdir, metavar='')
    # parser.add_argument('', '--url', help='url of the playlist to be downloaded', default='https://www.youtube.com/watch?v=kN6mlybyTdA', metavar='')
    args = parser.parse_args()

    PytHelper(args.playlisturl, args.destination)
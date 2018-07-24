# -*- coding: utf-8 -*-
import os, sys, time
import argparse
from urllib import urlopen
from pytube import YouTube
# import re
# from urllib2 import urlopen

class PytHelper(YouTube):
    'Sub Class'

    def __init__(self, arguments=[], defer_prefetch_init=False):
        self.dfaultPlayListUrl = 'https://www.youtube.com/watch?v=2NR1FOoSPio&list=PLzMlWTOO8JNB6wjaz1WI2dZrtZ9-T6cSj'
        self.url = arguments[1] if len(arguments) > 1 else self.dfaultPlayListUrl
        # print self.url
        # sys.exit(1)
        YouTube.__init__(self, self.url, defer_prefetch_init)

        # self.playListUrlPrefix = ''
        self.playList = []
        self.args = arguments
        self.startTime = ''

        self.main()

    def main(self):
        if len(self.getList(self.url)) > 0:
            self.playList = self.extractPlayList(self.url)
            print('This is playlist!!!', self.playList)
        #self.startTime = time.time()

        if os.path.exists(os.path.curdir):
                directory_contents = [f.split('.mp4',1)[0] for f in os.listdir(os.path.curdir) if f.endswith('.mp4')]
        else:
            print('Destination directory does not exist')
            sys.exit(1)

        # confirmation = raw_input("You are about to download {0} videos to {1}\nWould you like to continue? Y/n ".format(len(self.playList), os.path.abspath(args.destination)))
        confirmation = raw_input("You are about to download {0} videos to {1}\nWould you like to continue? Y/n ".format(len(self.playList), os.path.abspath(os.path.curdir)))
        
        if confirmation.lower() in ['y', '']:
            if len(self.playList) > 0:
                for u in self.playList:
                    yt = YouTube(u)
                    vid = yt.streams.filter(mime_type='video/mp4').order_by('resolution').last()
                    if vid.default_filename in directory_contents:
                        print('Skipping {}'.format(vid.default_filename))
                        # whats this??
                        continue
                    else:
                        print('Downloading {}'.format(vid.default_filename))
                        # vid.download(args.destination) 
                        vid.download(os.path.curdir) 
                        print('Done')
            else:
                vid = self.streams.filter(mime_type='video/mp4').order_by('resolution').last()
                if vid.default_filename in directory_contents:
                    print('Skipping {}'.format(vid.default_filename))
                else:
                    print('Downloading {}'.format(vid.default_filename))
                    # vid.download(args.destination) 
                    vid.download(os.path.curdir) 
                    print('Done')

		
        
    @staticmethod
    def getList(url):
        param = []
        qstr = url[url.find('?')+1:]
        for el in qstr.split('&'):
            if 'list' in el.split('='):
                param.append('https://www.youtube.com/playlist?{0}'.format(el))
        return param
    
    @staticmethod
    def extractPlayList(url):
        playList = []
        for line in urlopen(url).readlines():
            tag = line.decode('utf8')
            if 'pl-video-title-link' in tag:
                playList.append('https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0])

        return playList

if __name__ == "__main__" :
    arguments = sys.argv if len(sys.argv) > 1 else []

    PytHelper(arguments)

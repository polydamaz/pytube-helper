# -*- coding: utf-8 -*-
import os, sys, time
import argparse
from urllib import urlopen
from pytube import YouTube
# import re
# from urllib2 import urlopen

class PytHelper(YouTube):
    'Sub Class'
    def __init__(self, url, downloadDir, defer_prefetch_init=False):
        YouTube.__init__(self, url, defer_prefetch_init)
        
        self.url = url
        self.downloadDir = downloadDir
        self.playList = []
        self.playListURL = ''
        
        self.main()

    def main(self):

        if os.path.exists(self.downloadDir):
            directory_contents = [f.split('.mp4',1)[0] for f in os.listdir(self.downloadDir) if f.endswith('.mp4')]
        else:
            print('Destination directory does not exist')
            sys.exit(1)

        confirmation = raw_input("You are about to download {0} videos to {1}\nWould you like to continue? Y/n ".format(len(self.playList), os.path.abspath(self.downloadDir)))
        
        if confirmation.lower() in ['n']:
            print 'GoodBye'
            sys.exit()
        
        self.playListURL = self.getList(self.url)

        if self.playListURL:
            self.playList = self.extractPlayList(self.playListURL)
        else: 
            self.playList.append(self.url)

        for u in self.playList:
            yt = YouTube(u)
            vid = yt.streams.filter(mime_type='video/mp4').order_by('resolution').last()
            if vid.default_filename in directory_contents:
                print('Skipping {}'.format(vid.default_filename))
                continue
            else:
                print('Downloading {}'.format(vid.default_filename))
                vid.download(self.downloadDir) 
                print('Done')
		
        
    @staticmethod
    def getList(url):
        qstr = url[url.find('?')+1:]
        for el in qstr.split('&'):
            if 'list' in el.split('='):
                return 'https://www.youtube.com/playlist?{}'.format(el)
        
    
    @staticmethod
    def extractPlayList(url):
        playList = []
        for line in urlopen(url).readlines():
            tag = line.decode('utf8')
            if 'pl-video-title-link' in tag:
                playList.append('https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0])

        return playList

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-p PLAYLISTURL] [-d DESTINATION]')
    parser.add_argument('-p', '--playlisturl', help='url of the playlist to be downloaded', default='https://www.youtube.com/watch?v=aWrZ1QDs1tQ', metavar='')
    parser.add_argument('-d', '--destination', help='path of directory to save videos to', default=os.path.curdir, metavar='')
    args = parser.parse_args()

    PytHelper(args.playlisturl, args.destination)

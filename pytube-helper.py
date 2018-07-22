# -*- coding: utf-8 -*-
import os, sys, time
import argparse

# import re
# from urllib2 import urlopen

import sys

from urllib import urlopen
from pytube import YouTube

class PytHelper(YouTube):
    'Sub Class'

    def __init__(self, arguments=[], defer_prefetch_init=False):
        self.dfaultPlayListUrl = 'https://www.youtube.com/watch?v=2NR1FOoSPio&list=PLzMlWTOO8JNB6wjaz1WI2dZrtZ9-T6cSj'
        self.url = arguments[0] if len(arguments) > 1 else self.dfaultPlayListUrl

        YouTube.__init__(self, self.url, defer_prefetch_init)

        self.playListUrlPrefix = ''
        self.playList = []
        self.args = arguments
        self.startTime = ''

        self.main()

    def main(self):
        if self.__hasList() is True:
            self.__extractPlayList()
            print('This is playlist!!!', self.playList)
        else:
            print('This is Not playlist!!!')
        
        #self.startTime = time.time()

        """ 질의 """
        parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-p PLAYLISTURL] [-d DESTINATION]')
        parser.add_argument('-p', '--playlisturl', help='url of the playlist to be downloaded', default=self.dfaultPlayListUrl, metavar='')
        parser.add_argument('-d', '--destination', help='path of directory to save videos to', default=os.path.curdir, metavar='')
        args = parser.parse_args()

        if os.path.exists(args.destination):
                directory_contents = [f.split('.mp4',1)[0] for f in os.listdir(args.destination) if f.endswith('.mp4')]
        else:
            print('Destination directory does not exist')
            sys.exit(1)

        confirmation = raw_input("You are about to download {0} videos to {1}\nWould you like to continue? Y/n ".format(len(self.playList), os.path.abspath(args.destination)))
        
        if confirmation.lower() in ['y', '']:
            for u in self.playList:
                yt = YouTube(u)
                vid = yt.streams.filter(mime_type='video/mp4').order_by('resolution').last()

		if vid.default_filename in directory_contents:
			print('Skipping {}'.format(vid.default_filename))
			continue
		else:
			print('Downloading {}'.format(vid.default_filename))
			vid.download(args.destination)
			print('Done')
        

    # @staticmethod
    # def print_dot(bytes_received, file_size, start):
    #     if time.time() - start > 1.0:
    #         sys.stdout.write('.')
    #         sys.stdout.flush()
    #         start = time.time()


    # @staticmethod
    def __hasList(self):
        """ str find 와 split """
        urlParam = self.url[self.url.find('?')+1:]
        for el in urlParam.split('&'):
            if 'list' in el.split('='):
                self.playListUrlPrefix = 'https://www.youtube.com/playlist?{0}'.format(el)
                return True

        return False

    # @staticmethod
    def __extractPlayList(self):
        for line in urlopen(self.playListUrlPrefix).readlines():
            tag = line.decode('utf8')
            if 'pl-video-title-link' in tag:
                self.playList.append('https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0])

        print self.playList


if __name__ == "__main__" :
    arguments = sys.argv if len(sys.argv) > 1 else []

    PytHelper(arguments)

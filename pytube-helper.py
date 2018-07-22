# -*- coding: utf-8 -*-
import os, sys, time
# import argparse

# import re
# from urllib2 import urlopen

import sys

from urllib import urlopen
from pytube import YouTube

class PytHelper(YouTube):
    'Sub Class'

    def __init__(self, url=None, defer_prefetch_init=False):
        YouTube.__init__(self, url, defer_prefetch_init)
        self.url = url
        self.playListURL = ''
        self.playList = []
        
        if self._hasList() is True:
            print('This is playlist!!!')
            self._extractPlayList()
        else:
            print('This is Not playlist!!!')

    # @staticmethod
    def _hasList(self):
        """ str find 와 split """
        urlParam = self.url[self.url.find('?')+1:]
        for el in urlParam.split('&'): 
            if 'list' in el.split('='):
                self.playListURL = 'https://www.youtube.com/playlist?{0}'.format(el)
                return True

        return False

    # @staticmethod
    def _extractPlayList(self):
        # This is Like this Pattern -> https://github.com/svass/youtube-playlist-downloader/blob/master/playlist-downloader.py
        for line in urlopen(self.playListURL).readlines():
            tag = line.decode('utf8')
            if 'pl-video-title-link' in tag:
                self.playList.append('https://www.youtube.com' + tag.split('href="',1)[1].split('" ',1)[0])

        print self.playList


if __name__ == "__main__" :
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.youtube.com/watch?v=2NR1FOoSPio&list=PLzMlWTOO8JNB6wjaz1WI2dZrtZ9-T6cSj'

    PytHelper(url)

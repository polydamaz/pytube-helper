#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, argparse
from dialog import Dialog
from multiprocessing import Pool
import threading
from pytubeExtension import Playlist, Listitem, YouTube
from util import textLog

if __name__ == "__main__" :
    pyt = None
    lock = threading.Lock()
    # def perc(cur, total):
    #     return int((cur / total) * 100)

    # def progress_function(self, chunk, file_handle, bytes_remaining):
    #     if downloadList[nl]['siz'] is 0:
    #         downloadList[nl]['siz'] = self.filesize
            
    #     downloadList[nl]['per'] = int(perc(self.filesize - bytes_remaining, downloadList[nl]['siz']))
    #     dc['totPer'] = perc((nl * 100) + downloadList[nl]['per'], dc['totSum'])

    #     d.mixedgauge(
    #         text = '',
    #         elements = [(item['title'], '-' + str(item['per']) if type(item['per']) is int else item['per']  ) for item in downloadList],
    #         percent = dc['totPer'],
    #         title= pyt.listTitle
    #     )
    
    # def culc():
    #     numOfDnItems = 0
    #     totSum = 0 
    #     for i in self.__items:
    #         if i.confirmDn:
    #             totSum += i.cur
    #             numOfDnItems += 1
        
    #     if totSum == 0 or numOfDnItems == 0:
    #         return 0
    #     else:
    #         return (((numOfDnItems * 100) + totSum) / totSum) * 100

    # d_list = []

    def test():
        # d.mixedgauge(
        #     text = '',
        #     elements = [(n.title, n.status) for n in d_list ],
        #     percent = 100, #int(pyt.perc()),
        #     title = pyt.listTitle
        # )
        d.mixedgauge(
            text = '',
            elements = [(n.title, n.status) for n in pyt.items if n.confirmDn],
            percent = int(pyt.perc()),
            title = pyt.listTitle
        )
        # a = [(n.title, n.status) for n in pyt.items if n.confirmDn]
        # b = [(n.title, n.status) for n in d_list if n.confirmDn]
        # print('@@', d_list)

    def progress_function(self, chunk, file_handle, bytes_remaining):
        cur = int(((self.filesize - bytes_remaining) / self.filesize) *100)
        eleCurrent = ''
        i = [ int(item.code) for item in pyt.items if self.player_config_args['video_id'] == item.vid ][0]
        pyt.items[i].cur = cur
        # d_list[i]['cur'] = cur
        # pyt.setItem(i, 'cur', cur)

        if cur == 100 or cur == 'Complete':
            eleCurrent = 'Complete'
        else:
            eleCurrent =  '-' + str(cur)

        # playList[i].status = eleCurrent
        # playList[i].status = eleCurrent
        # pyt.setItem(i, 'status', eleCurrent)
        pyt.items[i].status = eleCurrent
        # d_list[i]['title'] = pyt.items[i].title
        # d_list[i]['status'] = eleCurrent

        # if pyt.selfTimer % 10 == 0:
        # test(i)
        lock.acquire()
        try:
            dnElements = [(n.title, n.status) for n in pyt.items if n.confirmDn]
            perc = int(pyt.perc())
            # numOfDnItems, totSum = pyt.perc()
            # if totSum == 0 or numOfDnItems == 0:
            #     perc = 0
            # else:    
            #     perc = (((numOfDnItems * 100) + totSum) / totSum) * 100
        finally:
            lock.release()

        d.mixedgauge(
            # text = 'numOfDnItems={}, totSum={}'.format(numOfDnItems, totSum),
            text = '',
            elements = dnElements,
            percent = perc,
            title = pyt.listTitle
        )

        # pyt.selfTimer += 1

    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-p PLAYLISTURL] [-d DESTINATION]')
    parser.add_argument('-p', '--playlisturl', help='url of the playlist to be downloaded', default='', metavar='')
    parser.add_argument('-d', '--destination', help='path of directory to save videos to', default=os.path.curdir, metavar='')
    args = parser.parse_args()

    url = ''
    d = Dialog(dialog="dialog")
    d.set_background_title("Pytube-extension: Youtube playlist Dowload")

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
    pyt = Playlist(url if url else args.playlisturl, path)
    d.infobox(text=m02)

    m03 = u"다운받을 영상을 선택하세요."
    code, tags = d.checklist(m03, choices=[(item.code, item.title, True) for item in pyt.items])

    pyt.downloadCheckTags(tags=tags)
    

    d.infobox(text=m02)
    if code == d.OK:
        # playList = pyt.items
        def downloadFnc(item):
            pyt.downloadConfirm(int(item.code), True,on_progress_callback=progress_function)
        
        # pool = Pool(processes=3)
        # pool.map(downloadFnc, pyt.items)
        for n in pyt.items:
            doenloadThread = threading.Thread(target=downloadFnc, args=(n,))
            doenloadThread.start()

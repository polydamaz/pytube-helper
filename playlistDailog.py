#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, argparse
from dialog import Dialog
from multiprocessing import Pool
import threading
from pytubeExtension import Playlist, Listitem, YouTube

if __name__ == "__main__" :
    def progress_function(self, chunk, file_handle, bytes_remaining):
        lock.acquire()
        cur = int(((self.filesize - bytes_remaining) / self.filesize) *100)
        i = [ int(item.code) for item in pyt.items if self.player_config_args['video_id'] == item.vid ][0]        
        pyt.items[i].cur = cur

        if cur == 100:
            eleCurrent = 'Complete'
        else:
            eleCurrent =  '-' + str(cur)

        pyt.items[i].state = eleCurrent
        
        try:
            dnElements = [(n.title, n.state) for n in pyt.items if n.confirmDn]
            perc = int(pyt.perc())
        finally:
            lock.release()
        
        d.mixedgauge(
            text = '',
            elements = dnElements,
            percent = perc,
            title = pyt.listTitle
        )

    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-p PLAYLISTURL] [-d DESTINATION]')
    parser.add_argument('-p', '--playlisturl', help='url of the playlist to be downloaded', default='', metavar='')
    parser.add_argument('-d', '--destination', help='path of directory to save videos to', default=os.path.curdir, metavar='')
    args = parser.parse_args()

    d = Dialog(dialog="dialog")
    d.set_background_title("Pytube-extension: Youtube playlist Dowload")

    processingMsg = u"처리중입니다."
    if args.playlisturl is '':
        code, url = d.inputbox(text=u"주소 입력", width=50)
        if code is d.CANCEL:
            print(u"사용자에의해 취소 되었습니다.")
            sys.exit()
    else:
        d.infobox(text=processingMsg)

    code, path = d.dselect(filepath=os.path.abspath(args.destination), width=50)
    if code == d.CANCEL:
        print(u"사용자에의해 취소 되었습니다.")
        sys.exit()

    """
    주소를 arguments로 직접 입력하였을시 빈 화면이 오래 보여지는 것 대신 처리중 문구를 보여 주기 위함.
    """
    d.infobox(text=processingMsg)
    pyt = Playlist(url if url else args.playlisturl, path)
    d.infobox(text=processingMsg)

    code, tags = d.checklist(u"다운받을 영상을 선택하세요.", choices=[(item.code, item.title, True) for item in pyt.items])
    
    pyt.checkDownload(tags=tags)

    d.infobox(text=processingMsg)
    if code == d.OK:
        lock = threading.Lock()

        def downloadFnc(item):
            pyt.download(int(item.code), on_progress_callback=progress_function)
        
        for n in pyt.items:
            doenloadThread = threading.Thread(target=downloadFnc, args=(n,))
            doenloadThread.start()
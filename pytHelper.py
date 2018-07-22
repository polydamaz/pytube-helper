#!/usr/bin/python
from pytube import YouTube

# Define


# Basic Controll
def basic_control():
    yt = YouTube('https://www.youtube.com/watch?v=LzC4xW0gEMk')
    stream = yt.streams.first()
    stream.download()
    print('@@')


"""
 pytube.YouTube(url=None, defer_prefetch_init=False, on_progress_callback=None, on_complete_callback=None, proxies=None)
"""

def class_controll(args):
    yt = YouTube(args)
    
    print(yt.streams.count)

class_controll('https://www.youtube.com/watch?v=oPeSnz1ATMo&list=PLzMlWTOO8JNCYQjvV-f2EPVCoDdHSymii')
# class_controll('https://www.youtube.com/watch?v=LzC4xW0gEMk')
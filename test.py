import sys, os
# from pytHelper import PytHelper
from functools import reduce
from pytube import YouTube
from multiprocessing import Pool, Process, Queue

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()

sys.exit()
#########
arr = {'needle':0,'total':0}
listArr = list(range(100))
aa = 0
def product(*numbers):
    p = reduce(lambda x, y: x + y, numbers)
    return p

# print(product(*listArr))
# sys.exit()

def callbackFnc(q):
    # global arr
    # print(arr)
    # arr['needle'] = item
    # arr['total'] += item
    q.put([42, None, 'hello'])

def loofFnc(item):
    callbackFnc(item)

# pool = Pool(processes=3)
# pool.map(loofFnc, listArr)

q = Queue()
p = Process(target=loofFnc, args=(q,))
p.start()
print(q.get())    # prints "[42, None, 'hello']"
p.join()



print('@@',arr['needle'], arr['total'])
sys.exit()




vector_list = [[1, 2, 3]]
for i, vector in enumerate(vector_list * 3):
    print("{0} scalar product of vector: {1}".format((i + 1), [(i + 1) * e for e in vector]))

sys.exit()


# 길이 100의 제로값 리스트 초기화
zeros_list = [0] * 10

print(zeros_list)
# 길이 100의 제로값 튜플 선언
zeros_tuple = (0,) * 10
print(zeros_tuple)

print(2*3, 2**3)

sys.exit()



yt = YouTube("https://www.youtube.com/watch?v=NChP-7KMQ_U&list=PLuHgQVnccGMA5836CvWfieEQy0T0ov6Jh")
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('./')
# print(yt._monostate['player_config_args'])
print(yt.player_config_args['video_id'])
# pyt.__playListURL('url')
# playList = pyt.getPlayList()    
# pyt.playListURL = url
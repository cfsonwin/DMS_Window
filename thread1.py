import threading
import time
from queue import Queue
def Thr1():
    print('*****T1****\n', threading.current_thread(), '\n*****T1****')
    for i in range(10):
        time.sleep(0.1)
        print('waiting T1 ...')
    print('thread 1 end')

def Thr2():
    print('*****T2****\n', threading.current_thread(), '\n*****T2****')
    for i in range(10):
        time.sleep(0.1)
        print('waiting T2...')
    print('thread 2 end')
def main():
    # print(threading.active_count())
    # print(threading.enumerate())
    # print(threading.current_thread())
    added_thr1 = threading.Thread(target=Thr1, name = 'T1')
    added_thr1.start()
    added_thr2 = threading.Thread(target=Thr2, name='T1')

    added_thr1.join()
    added_thr2.start()
    added_thr2.join()
    print('all done')
    # print(threading.active_count())
    # print(threading.enumerate())
    # print(threading.current_thread())

def MultiT():
    pass

if __name__=='__main__':
    main()

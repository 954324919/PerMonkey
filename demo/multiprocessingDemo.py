#coding=utf-8
#多进程通信
from multiprocessing import Process,Queue,Pipe,Manager

def runMon(q):
    # if not q.full():
    #     q.put("执行完Monkey测试啦~")
    q.append("stop")
def adblog(q):
    # while not q.empty():
    #     z=q.get()
    #     print(z)
    while len(q)!=0:
        print("adb log要结束")
        break
def cpumem(q):
    while len(q)!=0:
        print("cpu mem要结束")
        break
if __name__=='__main__':
    '''
    q = Queue()
    
    mon=Process(target=runMon,args=(q,))
    log=Process(target=adblog,args=(q,))
    mon.start()
    log.start()

    mon.join()
    log.join()
    '''
    manager=Manager()
    li=manager.list()
    p1=Process(target=runMon,args=(li,))

    p2 = Process(target=adblog, args=(li,))
    p3=Process(target=cpumem, args=(li,))
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
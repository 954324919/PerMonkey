# -*- coding: utf-8 -*-

import subprocess,time,xml,datetime,os
from root import PROJECT_ROOT
from multiprocessing import Process,Queue,Manager
from log import osTest
from common.POUtils import ParseXml
from GenerateReport import main

from common.performance import Performance
xmlData=ParseXml().getXmlParser()
per=Performance()
log_c=osTest()
def runMonkey(q):
    f=open(PROJECT_ROOT+'/result/log/testMonkey.txt','a',encoding='utf-8')
    with open("whitelist.txt","w") as files:
        files.write(xmlData["Package"])

    os.system("adb push whitelist.txt /data/local/tmp")
    time.sleep(1)
    cmd = xmlData["monkeyCmd"] % (xmlData['Package'],xmlData['eventinterval'],xmlData['executeTotalAction'])
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in ps.stdout:
        li=line.decode()
        print(li,file=f)
        if li.count('Monkey finished')>0:
            q.append("stop")
            break
    f.close()
    # log_c.killADB()
def memRun(q):
    time.sleep(1)
    while True:
        if len(q)!=0:
            break
        per.writePerInfo()
    #写入到excel中
    per.writeExcel()

def run():
    per.init()
    # q=Queue()
    manager=Manager()
    q = manager.list()
    p1=Process(target=osTest().executeLog,args=(q,))
    p2=Process(target=runMonkey,args=(q,))
    p1.start()
    p2.start()

    if xmlData['type_name']=='performance':
        p3=Process(target=memRun,args=(q,))
        p3.start()
        p3.join()

    p1.join()
    p2.join()
    #调用下面方法生成html报告
    main()


if __name__=='__main__':
    run()
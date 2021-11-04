#coding=utf-8
import random,multiprocessing
import subprocess,checkport
from appium import webdriver
from adbUtils import ADB
def start_appium(host,port):
    bootstrap_port=port+1
    cmd='appium -a '+host+' -p '+str(port)+' --bootstrap-port '+str(bootstrap_port)
    print(cmd)
    subprocess.Popen(cmd,shell=True,stdout=open(str(port)+'.log','a'),stderr=subprocess.STDOUT)

def appium_server(port):
    adb=ADB()
    lis=adb.attached_devices()
    appium_process=[]
    if len(lis)!=0:
        for i in range(len(lis)):
            ip='127.0.0.1'
            port1=port+2*i
            if checkport.check_port(ip,port1):
                p=multiprocessing.Process(target=start_appium,args=(ip,port1))
                appium_process.append(p)
            else:
                checkport.release_port(port1)
    return appium_process
def start_appium_server(port):
    servers=appium_server(port)
    for appium in servers:
        appium.start()
    for appium in servers:
        appium.join()
if __name__ == '__main__':
    start_appium_server(4723)
#-** coding=utf-8 -*-
#coding=utf-8
import os
import subprocess
import sys
import time
import datetime,traceback
import xml.dom.minidom
import requests
from root import PROJECT_ROOT
from os.path import join,getsize
import platform
from common.POUtils import ParseXml
logDir=''
system = platform.system()
if system is "Windows":
    find_util = "\\"

else:
    find_util = "/"

result_dir = PROJECT_ROOT + find_util+'result'+find_util
class osTest(object):
	def __init__(self):
		self.xmlData = ParseXml().getXmlParser()
		self.logpath = result_dir + 'log'
		if not os.path.exists(self.logpath):
			os.makedirs(self.logpath)
		self.isCancel=True
	def crashFile(self):
		mytime=str(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))
		myfilename=self.logpath+find_util+mytime+'crash.txt'
		return myfilename
	def anrFile(self,traces):

		mytime=str(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))
		if traces=='traces':
			myfilename=self.logpath+find_util+mytime+'anr_traces.txt'
			return myfilename
		if traces=='bugreport':
			myfilename=self.logpath+find_util+mytime+'tracesbugreport.txt'
			return myfilename
	def getLogFile(self):
		mytime=str(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))
		myfilename=self.logpath+find_util+mytime+'.txt'
		return myfilename
	def killADB(self):
		if system is "Windows":
			ps = subprocess.Popen('netstat -aon|findstr 5037', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
			for line in ps.stdout:
				lst = []
				line = line.decode()
				if line.find('LISTENING') != -1:
					for i in line.split(' '):
						if i:
							lst.append(i)
					port = lst[-1]
					subprocess.Popen('taskkill /f /t /im ' + port, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
									  shell=True)
					break
		else:
			ps=subprocess.Popen('lsof -i tcp:5037',stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
			for line in ps.stdout:

				lst=[]
				line=line.decode()
				if line.find('LISTEN')!=-1:
					for i in line.split(' '):
						if i:
							lst.append(i)
					# print(lst)
					port =lst[1]  #通过查看命令行得知 第二个参数是端口号
					# subprocess.Popen('kill -9 '+port,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
					os.system('kill -9 '+port)
					break
	def executeLog(self,q):
		time.sleep(5)
		ps=subprocess.Popen('adb logcat -v time',stdout=subprocess.PIPE,shell=True).stdout
		startTime=datetime.datetime.now()
		while True:
			'''
			expectTime = self.xmlData['executeTotalTime']
			executeTime = datetime.datetime.now()
			TheTime = (executeTime - startTime).seconds
			if TheTime > int(expectTime):
				break
			'''
			ss = self.getLogFile()
			Logtest = open(ss, "a", encoding='utf-8')

			for line in ps:
				try:
					if len(q)!=0:  #多进程之间通信
						return  #直接跳出多层循环，无需再kill adb
					'''
					executeTime=datetime.datetime.now()
					TheTime=(executeTime - startTime).seconds
					if TheTime > int(expectTime):
						break
					'''
					if getsize(ss)<1024*1024*10:
						li=line.decode('utf-8','ignore')
						print(li,file=Logtest)
						'''
						if line.find('ANR:')!=-1 and line.find('ANRManager')==-1:  #anr判断
							time.sleep(1)
							traceslog=subprocess.Popen("adb shell ls /data/anr/traces.txt",shell=True,stdout=subprocess.PIPE,
								stderr=subprocess.PIPE).stdout.read()
							tracesreportlog=subprocess.Popen("adb shell ls /data/anr/traces.txt.bugreport",shell=True,stdout=subprocess.PIPE,
								stderr=subprocess.PIPE).stdout.read()
							if 'No such file or directory' not in traceslog:  #存在traces.txt文件

								os.system("adb shell cat /data/anr/traces.txt > "+self.anrFile("traces"))
							if 'No such file or directory' not in tracesreportlog:  #存在bugreport文件

								os.system("adb shell cat /data/anr/traces.txt.bugreport > "+self.anrFile("bugreport"))
						'''
						if li.find('FATAL EXCEPTION')!=-1 or (li.find('ANR:')!=-1 or li.find('Fatal signal')!=-1 and li.find('ANRManager')==-1):
							s=0
							crashFile=open(self.crashFile(),"a",encoding='utf-8')
							print("发生Crash或者ANR的Log信息如下："+"\n\n",file=crashFile)
							for line in ps:
								li=line.decode('utf-8','ignore')
								if s<=100:
									print(li,file=crashFile)
								else:
									crashFile.close()
									if len(q)!=0:
										return  # 直接跳出多层循环，无需再kill adb
								s+=1
							os.popen('adb logcat -c')
							break
					else:
						os.popen('adb logcat -c')
						break

				except Exception as e:
					traceback.print_exc()
					print(e)

if __name__ == '__main__':
	osTest().killADB()
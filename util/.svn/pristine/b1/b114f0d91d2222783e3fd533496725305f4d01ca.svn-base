#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇

import Queue
#严格按小时/天输出文件,必然有上层目录装在一起
#只按大小输出到文件,超出512M才换文件,不需要目录装
if 'gbOnce' not in globals():
	gbOnce=True
	
	gQueue=Queue.Queue()
	gThread=None

def initDirStartThread(sRootDir):
	global gsRootDir
	global gThread
	gsRootDir=sRootDir
	
	gThread=threading.Thread(None,__logProc) #gThread=thread.start_new_thread(__logProc,())
	#gThread.setDaemon(False)
	gThread.start()	
	
#sPrefixFormat传空表示不加时间前缀
#sPathName不要加后缀,会自动加.log作为后缀
#sPathName 可以是 file 或者 dir1/file 或者 dir1/dir2/file
#sContent最后一个字符如何不是\n,则会自动加一个\n
def log(sPathName,sContent,sPrefixFormat='%Y-%m-%d %H:%M:%S'):
	if not sContent:
		return
	if gThread is None:
		raise Exception,'log线程尚未启动或已关闭.'
# 	lPathName=sPathName.split('/')
# 	if len(lPathName)>1:
# 		sFileName=lPathName[len(lPathName)-1]
# 	else:
# 		sFileName=sPathName
	
	fStamp=gevent.core.time()
	if sPrefixFormat:
		sPrefix=time.strftime(sPrefixFormat,time.localtime(fStamp)) #每一行的前缀
		sContent="[%s]%s"%(sPrefix,sContent)
	
	sPathName='../{}/{}'.format(gsRootDir,sPathName)
	gQueue.put((sPathName,fStamp,sContent))

def closeAll():#关闭全部文件.
	global gThread
	if gThread==None:
		return
	gQueue.put(STOP)
	gThread.join()
	gThread=None

def __logProc(*tArgs):	
	dFileDescriptor={}
	while True:
		tInfo=gQueue.get()
		if tInfo==STOP:			
			break
		sPathName,fStamp,sContent=tInfo
		oFile,iLastCycle=dFileDescriptor.get(sPathName,(None,0))
		if not oFile:#还没有打开文件,有可能连目录都没有
			sDirName=os.path.dirname(sPathName)
			if sDirName and not os.path.exists(sDirName):#如果目录不存在则创建目录
				os.makedirs(sDirName)

		iCurCycle=int(fStamp)%3600 #小时周期
		if (oFile==None or iLastCycle==0) or iLastCycle!=iCurCycle:#从未打开过文件 或 切换小时了
			dFileDescriptor.pop(sPathName,None)
			if oFile:
				oFile.close()

# 			sFullPathName=time.strftime('{}.%Y-%m-%d-%H.log',time.localtime(fStamp)).format(sPathName)#log文件名要带上时间
			sFullPathName=sPathName+".log"
			oFile=open(sFullPathName,'a',10*1024)#
			dFileDescriptor[sPathName]=oFile,iCurCycle
		if sContent[-1]=='\n':
			oFile.write(sContent)
		else:
			oFile.write(sContent+'\n')
		oFile.flush()

	#break出来后全部文件关闭
	for oFile,iLastCycle in dFileDescriptor.itervalues():
		oFile.close()

def getNeedWriteSize():#获得待写入的条目数量
	return gQueue.qsize()

STOP=(None,None,None,None)

import thread
import threading

import time
import os.path
import gevent
import u

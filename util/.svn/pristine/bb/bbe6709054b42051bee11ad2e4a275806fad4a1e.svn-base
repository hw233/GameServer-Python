#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇

CONNECTED=0 #已连接
CONNECTING=1 #连接中
DISCONNECTED=2 #未连接


#断开连接后会分别间隔1,2,4,8,16,32,64,128秒后重试.
#所以要有马上重试的接口.免得修复网络连接后还得等n秒才能连得上.

class cStreamClient(object):
	def __init__(self,tlAddress,cHandle):
		self.tlAddress=tlAddress
		self.cHandle=cHandle
		self.iStatus=DISCONNECTED
		self.ep=None
		self.fMinDelay=1
		self.fMaxDelay=64
		self.fDelay=self.fMinDelay

	def status(self):
		return self.iStatus

	def connect(self,iRetryTimes=1):#iRetryTimes 尝试连接次数,0表示无限次数
		if self.ep:
			return True
		if self.iStatus in (CONNECTED,):
			return True
		self.iStatus=CONNECTING		
		bInfinite=True if iRetryTimes==0 else False
		while bInfinite or iRetryTimes>0:
			try:
				if not bInfinite:
					iRetryTimes-=1
				sk=gevent.socket.create_connection(self.tlAddress)
				self.fDelay=self.fMinDelay #成功了,改小再次重试的值
				self.iStatus=CONNECTED
				break
			except socket.error,value:
				print '{}:连接失败:{},{}秒后将再次尝试.'.format(timeU.stamp2str(),value,self.fDelay)
				#要记log
				gevent.sleep(self.fDelay)
				self.fDelay=min(self.fMaxDelay,self.fDelay*2)#下一次重试失败后的等待时间
				continue
			except Exception:
				self.iStatus=DISCONNECTED
				raise
		else:
			return False#尝试次数用完了都还没有连成功
		self.ep=self.cHandle(sk,self.tlAddress)
		self.ep.eDisConnected+=self.disConnectedEventHandler
		return True

	def disConnectedEventHandler(self,ep):
		self.iStatus=DISCONNECTED
		self.ep=None

def shortConnectionSend(tlAddress,sRequest):#短连接发送,服务器主动关闭
	sk=gevent.socket.create_connection(tlAddress)
	sk.sendall(sRequest)
	lRespond=[]
	while True:#短连接,要用while循环接收,直到收到fin分节,即是空字符串.
		sTemp=sk.recv(128*1024)#
		if not sTemp:#服务器关闭连接后，会收到一个空字符''
			sk.close()
			break
		lRespond.append(sTemp)
	return ''.join(lRespond)

import sys
import traceback
import socket
import gevent
import gevent.socket
import gevent.queue

import u
import log
import timeU
#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import client
import endPointWithSocket
#import service_pb2

#模拟游戏客户端,用于测试

import svcLogin
class combineService(
	#svcLogin.cService,
	):
	pass


class cEndPointWithSocket(endPointWithSocket.cEndPointWithSocket):
	def __init__(self,iServiceNo,*tArgs,**dArgs):
		self.iServiceNo=iServiceNo
		endPointWithSocket.cEndPointWithSocket.__init__(self,*tArgs,**dArgs)

	def _onDisConnected(self):
		endPointWithSocket.cEndPointWithSocket._onDisConnected(self)
		sText='与{}号登录服{}:{}的连接断线了.'.format(self.iServiceNo,self.ip(),self.iPort)
		print sText
		log.log('info',sText)
		gdLoginChn.pop(self.iServiceNo,None)		
		#断线了,要尝试重连.


def autoInit():	
	return
	startCheck()

def startCheck():#启动时检查登录服务器,只是检查提示写log,不影响启服流程
	try:
		configChn=clientConfig.endPoint#要想知道登录服的信息,要去配置服务器上去查
	except Exception,e:		
		print str(e)
		return
	bFail,uMsg=configChn.rpcQueryServer(0,config_pb2.ST_LOGIN,config_pb2.CT_LOGIC)#查询ip与端口,0表示全部
	if bFail:
		print '查询配置服务器失败:{}'.format(uMsg.sReason)
		return
	if len(uMsg.ports)==0:
		print '尚未启动登录服,请稍候启动登录服.'

	for info in uMsg.ports:
		iServiceNo,sIP,iPort=info.iServiceNo,info.sIP,info.iPort	
		print ('login client:starting try to connect to ip:{} port:{}'.format(sIP,iPort))
		try:
			sock=gevent.socket.create_connection((sIP,iPort))
		except Exception:
			print '连接登录服务器失败.ip:{},port:{}'.format(sIP,iPort)
			return
		bDebugMode=True		
		#loginChn=cEndPointWithSocket(iServiceNo,bDebugMode,(combineService,service_pb2.logicServer_loginServer_Stub))	
		loginChn.setIP(sIP).setPort(iPort).setSocket(sock)
		loginChn.start()
		gdLoginChn[iServiceNo]=loginChn
	



def getEndPoint(iLoginServiceNo=1):#连接登录服务器
	if iLoginServiceNo==0:
		raise Exception,'参数不可以是0'

	if iLoginServiceNo not in gdLoginChn:
		configChn=clientConfig.endPoint#要想知道登录服的信息,要去配置服务器上去查

		bFail,uMsg=configChn.rpcQueryServer(iLoginServiceNo,config_pb2.ST_LOGIN,config_pb2.CT_LOGIC)#查询ip与端口
		if bFail:
			raise Exception,'查询配置服务器失败:{}'.format(uMsg.sReason)
		#print 'uMsg',uMsg
		for info in uMsg.ports:
			iServiceNo,sIP,iPort=info.iServiceNo,info.sIP,info.iPort
			if iServiceNo!=iLoginServiceNo:
				raise Exception,'不可能'
			else:
				break
		else:
			raise Exception,'配置服务器回答说:{}号登录服没有启动'.format(iLoginServiceNo)
		
		print ('login client:starting try to connect to ip:{} port:{}'.format(sIP,iPort))
		try:
			sock=gevent.socket.create_connection((sIP,iPort))
		except Exception:
			u.reRaise('连接登录服务器失败.ip:{},port:{}'.format(sIP,iPort))
			
		bDebugMode=True		
		#loginChn=cEndPointWithSocket(iLoginServiceNo,bDebugMode,(combineService,service_pb2.logicServer_loginServer_Stub))	
		loginChn.setIP(sIP).setPort(iPort).setSocket(sock)
		loginChn.start()
		gdLoginChn[iLoginServiceNo]=loginChn
		log.log('info','连接{}号登录服{}:{}成功'.format(iLoginServiceNo,sIP,iPort))
	return gdLoginChn[iLoginServiceNo]


import platform
import socket
import traceback
import gevent
import gevent.socket

import misc
import u
import log

#import config_pb2

if 'gbOnce' not in globals():
	gbOnce=True

	if 'mainService' in SYS_ARGV:
		gdLoginChn={} #登录服channel,假设有多个登录服

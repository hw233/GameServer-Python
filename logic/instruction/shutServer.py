#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def broadcastShutGSMsg():#给在线玩家发送关服命令
	oMsg=common_pb2.bytes_()
	oMsg.sValue='游戏即将停机维护!请稍候登录,感谢广大玩家拥护.'
	role.roleHelper.worldBroadcast('rpcTips',oMsg)
	role.roleHelper.worldBroadcast('rpcSysPrompt',oMsg)
	oReloginMsg = common_pb2.reloginMsg()
	oReloginMsg.sContent='服务器已重启，请重新登录！'
	oReloginMsg.iType=1
	role.roleHelper.worldBroadcast('rpcReloginMsg',oReloginMsg)

def kickAllRole(sDelayKillChn=[]):#剔除玩家下线,sDelayKillChn忽略的玩家列表
	log.log('shutServer', 'kickAllRole started')
	lJob=[]
	for iEndPointId,oChn in tuple(mainService.gEndPointKeeper.getIterItems()):
		if oChn not in sDelayKillChn:#
			job=gevent.spawn(u.cFunctor(oChn.shutdown),5)
			lJob.append(job)
	gevent.joinall(lJob,None,True)
	log.log('shutServer', 'kickAllRole done')

def saveAllData():#停服之前保存各种数据
	for oSingleton in block.singleton.glSingleton:#存盘各个singleton对象(各种排行榜,物品交易所,钻石交易所)
		oSingleton._saveToDB()
	log.log('shutServer', 'save singleton done')
	#等等实例踢出内存,会自动保存	
	for oKeeper in productKeeper.glProductKeeper:
		if oKeeper==account.gKeeper:#账号keeper最后再清理,因为remove角色时要访问账号对象(有依赖关系)
			continue
		oKeeper.removeAllObj()
	log.log('shutServer', 'remove productKeeper done')
	account.gKeeper.removeAllObj()	
	log.log('shutServer', 'saveAllData done')

def stopAllServer():
	for oServer in init.glServers:#各个服务不再监听端口
		oServer.stop()

def onCaptureSigterm(*args):#截取到系统信号
	# if iSgiNo!=signal.SIGTERM:#不是SIGTERM信号
	# 	return
	broadcastShutGSMsg()

	kickAllRole()
	log.log('shutServer', '信号kill掉服务进程______________________1')
	# lChnds=mainService.gEndPointKeeper.getKeys()
	# if lChnds:
	# 	kickAllRole([mainService.gEndPointKeeper.getObj(lChnds[len(lChnds)-1])])
	block.sysActive.gActive.onStopServer()
	saveAllData()
	log.log('shutServer', '信号kill掉服务进程______________________2')
	stopAllServer()
	# ep=mainService.gEndPointKeeper.getObj(lChnds[len(lChnds)-1])
	# if ep:
	# 	ep.shutdown()
	# statistics.onShutServer()
	log.log('shutServer', '信号kill掉服务进程______________________3')	#
	# log.log('ddic/shutServer','\t{}'.format(''))

	#sys.exit(0)

def onSceneServiceCaptureSigterm(*args):#场景服截取到系统信号
	# if iSgiNo!=signal.SIGTERM:#不是SIGTERM信号
	# 	return
	log.log('shutServer', '信号kill掉服务进程______________________1')
	stopAllServer()
	log.log('shutServer', '信号kill掉服务进程______________________2')

	
import signal
import os
import platform
import gevent
import gevent.fileobject
import urllib2
import gevent.socket
import time

import timeU
import u
import log
import c
import misc
import npc
import scene
import makeData
import mainService
import role
import role.roleHelper
import account
import common_pb2
import props_pb2
import productKeeper
import factory
import mail
import types
import rank

import block.parameter
import block.singleton
import block.sysActive
import init
import sys
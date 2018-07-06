# -*- coding: utf-8 -*-

def init():
	global gClientList, gEndPointKeeper, gClientRoleList
	gClientList = {}
# 	gEndPointKeeper = keeper.cKeeper()
	gClientRoleList = {}

def getClient(accountName):
	'''获取客户端对象
	'''
	return gClientList.get(accountName)

def getClientRole(roleId):
	'''获取客户端角色对象
	'''
	return gClientRoleList.get(roleId)

def createClientRole(accountName, roleId):
	return robot.object.ClientRole(accountName, roleId)



def start(*args):
	robotCount = config.ROBOT_COUNT
	sPrefix='rbt'
	if args:
		if args[0].isdigit() and int(args[0]) > 0:
			robotCount = int(args[0])
		if len(args)>=2:
			sPrefix=args[1]


	jobList = []
	for i in xrange(robotCount):
		accountName = "%s%05d" % (sPrefix,10000 + i + 1)
		jobList.append(gevent.spawn(_connect, accountName))
		if True or len(jobList) >= 6 or (i + 1) >= robotCount:
			gevent.joinall(jobList)
			jobList = []
# 			gevent.sleep(rand(5))

	writeLog("start", "start robot count: %d" % robotCount)
	waiter = gevent.event.Event()
	waiter.wait()
	
def _connect(accountName):
	'''连接
	'''
	ip = config.ROBOT_SERVER_IP
	port = config.ROBOT_SERVER_PORT
	clientObj = client.cStreamClient((ip, port), _afterConnect)
	gClientList[accountName] = clientObj
	
	clientObj.connect(0)
	clientObj.ep.accountName = accountName
	robot.accountSvc.rpcRobotLogin(clientObj.ep, accountName)
	
def _afterConnect(sock, addr):
	ip, port = addr
# 	print "robot client: connect success to ip:%s port:%s" % (ip, port)
	debugMode = False #config.IS_INNER_SERVER
	ep = robot.object.EndPointWithSocket(debugMode, robot.service.gtService)
	ep.setIP(ip).setPort(port).setSocket(sock)
	ep.start()
# 	gEndPointKeeper.addObj(ep, ep.epId())
	return ep

from common import *
from robot.defines import *
import gevent
import robotData
import config
import client
import robot.accountSvc
import robot.object
import robot.service
import timingWheel

# #-*-coding:utf-8-*-
# #作者:马昭@曹县闫店楼镇
# import client
# import endPointWithSocket
# import terminal_main_pb2
# import serviceMisc_pb2
# import account_pb2
# #机器人客户端,用于测试性能
# 
# bNotLog=True  #是否log了,当一个客户端连上服务器时,就把频率测试人数等发给客户端做好日记纪录
# gdAmountAndTime={}   #{id1:[次数,最后一次发包时间],id2:[次数,最后一次发包时间]}
# 
# import service
# class combineService1(
# 	service.cService1,
# 	):
# 	pass
#  
# class combineService2(
# 	service.cService2,
# 	):
# 	pass
#  
# class cEndPointWithSocket(endPointWithSocket.cEndPointWithSocket):
# 	def _onDisConnected(self):
# 		endPointWithSocket.cEndPointWithSocket._onDisConnected(self)
# 		print u.trans2gbk('机器人断线了.')
#  
# def afterConnect(sock,tAddress):
# 	sIP,iPort=tAddress
# 	print u.trans2gbk('robot client:connect success to ip:{} port:{}').format(*tAddress)	
# 	bDebugMode=config.IS_INNER_SERVER
# 	ep=cEndPointWithSocket(bDebugMode,(combineService1,terminal_main_pb2.gameServerService_Stub),(combineService2,serviceMisc_pb2.gameServerMiscService_Stub))
# 	ep.setIP(sIP).setPort(iPort).setSocket(sock)
# 	ep.start()
# 	return ep
#  
# def start(*tArgs):
# 	global gsTest
#  
# 		sIp,iPort=config.TEST_SERVER_IP,config.TEST_SERVER_PORT
# 	iStartId=config.TEST_SID
# 	iEndId=config.TEST_EID
# 	sTestType=config.TEST_ITEM
# 		 
# 		lAllTest=sTestType.split('|')
# 	dAllTest={}
# 	for sTest in lAllTest:
# 		lTemp=sTest.split(',')
# 		iTest=int(lTemp[0])
# 		if iTest not in gsTest:
# 			print u.trans2gbk('测试类型{}不存在,测试终止.'.format(iTest))
# 			return
# 		dAllTest[iTest]=float(lTemp[1])
# 	if 1 in dAllTest and len(dAllTest)>1:
# 		print u.trans2gbk('Login必须单独测试！')
# 		return
# 	#sIp='192.168.1.11'
# 	jobs=[]
# 	iLoopId=iStartId
# 	while iStartId<=iEndId:
# 		jobs=[]
# 		for iId in xrange(iStartId,iStartId+6):
# 			jobs.append(gevent.spawn(login,sIp,iPort,iId))
# 		gevent.joinall(jobs)
# 		iStartId+=6
#  
# 	for iId in xrange(iLoopId, iStartId):
# 		# gevent.spawn_later(0,testWalk,gdClient[iId],iId,dAllTest)	
# 		gevent.spawn_later(0,testClient,sIp,iPort,iId,dAllTest,iEndId-iStartId)
#  		
# 	# oFunc=u.cFunctor(setLog,iStartId,iEndId)
# 	# oTimerMng=timer.cTimerMng()
# 	# oTimerMng.run(oFunc,10,600)
# 	raw_input(u.trans('按任意键退出.'))
#  
#  
# 	sContent1='-----------------------------------------------------------\n测试总人数:{}'.format(iEndId-iStartId)
# 	sContent2=''
# 	l=gdAmountAndTime.keys()
# 	l.sort()
# 	for iId in l:
# 		lTimes=gdAmountAndTime.get(iId)
# 		sContent2+='\nid:{}  发包次数:{}  最后一次发包时间:{}'.format(iId,lTimes[0],lTimes[1])
# 	log.log('clientStressTest','{}{}'.format(sContent1,sContent2))
#  
# def sendToServer(ep,iTotal,dAllTest):
# 	global bNotLog
# 	if bNotLog:
# 		for iTest in dAllTest.iterkeys():
# 			ep.rpcSysState(iTest,1.1)
# 			bNotLog=False
#  
# def login(sIp,iPort,iId):
# 	# oTimerMng=timer.cTimerMng()
# 	oClient=client.cStreamClient((sIp,iPort),afterConnect)
# 	gdClient[iId]=oClient
# 	oClient.connect(0)
# 	oClient.ep.waiter=gevent.event.Event()
# 	oClient.ep.rpcAccountLogin(str(iId),'1000',2,'123','aaa','bbb')
# 	oClient.ep.waiter.wait()
#  
#  
# def testClient(sIp,iPort,iId,dAllTest,iTotal):
# 	oTimerMng=timer.cTimerMng()
# 	# oClient=client.cStreamClient((sIp,iPort),afterConnect)
# 	# gdClient[iId]=oClient
# 	# oClient.connect(0)
# 	# oClient.ep.waiter=gevent.event.Event()
# 	# oClient.ep.rpcAccountLogin(str(iId),'1000',2,'123','aaa','bbb')
# 	# oClient.ep.waiter.wait()
# 	# return
# 	# sendToServer(oClient.ep,iTotal,dAllTest)
# 	oClient=gdClient[iId]
# 	for iTest,fFrequency in dAllTest.iteritems():
# 		fRemainder=fFrequency%1	  #填1.28意味着每秒1.28次,将其改为每25秒7次
# 		if fRemainder>0:
# 			sFixedRemainder=str(fRemainder)[2:5] 	#小数点后两位0.28
# 			iFixedMultiple=10**len(sFixedRemainder)	#10的小数点后位数的次方,0.28转化为28/100,0.3则转为3/10,0.125转为125/1000,超出位舍弃
# 			iGcd=gcd(int(sFixedRemainder),iFixedMultiple) 	#28/100的最大公约数4,约分后7/25,即小数点后的0.28次/秒转化为7次/25秒
# 			iInterval=iFixedMultiple/iGcd					#间隔从1秒变为25秒
# 		else:
# 			iInterval=1
# 		iFrequency=int(fFrequency*iInterval)				#一共1.28*25=32次/25秒
# 		if iTest==1:
# 			oFunc=u.cFunctor(rpcLogin,oClient,iId)
# 		elif iTest==2:
# 			oFunc=u.cFunctor(rpcWalk,oClient,iId)
# 		elif iTest==3:
# 			oFunc=u.cFunctor(rpcTalk,oClient,iId)
# 		elif iTest==4:
# 			oFunc=u.cFunctor(rpcSwitchMap,oClient,iId)
#  
# 		# oFuncPerSecond=u.cFunctor(randomPerSecond,oTimerMng,iInterval,iFrequency,oFunc)
# 		# oTimerMng.run(oFuncPerSecond,1,iInterval)
# 		oDelayFunc=u.cFunctor(funcLoop,oFunc,1/fFrequency,iId)
# 		oTimerMng.run(oDelayFunc,1)
#  
# 	while 1:
# 		raw_input()
#  
# def gcd(a,b):
# 	if a==0:
# 		return b
# 	else:
# 		return gcd(b%a,a)
#  
# def randomPerSecond(oTimerMng,iInterval,iFrequency,oFunc):
# 	# lDelay=[random.random()*iInterval for i in xrange(iFrequency)]
# 	# for iDelay in lDelay:
# 	# 	oTimerMng.run(oFunc,iDelay)
# 	iPerFre=iInterval/iFrequency
# 	for i in xrange(iFrequency):
# 		iDelay=(random.random()+i)*iPerFre
# 		oTimerMng.run(oFunc,iDelay)
#  
# def funcLoop(oFunc,iDelay,iId):
# 	while True:
# 		iRandomDelay=iDelay*2*random.random()  #如果是0.5秒触发一次的话,就在0~1秒内随机一个时间
# 		oFunc(iRandomDelay)
# 		gevent.sleep(iRandomDelay)
#  
# def rpcLogin(iDelay,oClient,iId):
# 	bFail,uResponse=oClient.ep.rpcForceRemoveRole()
# 	addTimes(iId,False)
# 	if bFail:
# 		print u.trans2gbk('{}强制退出角色失败'.format(iId))
# 	elif uResponse.iValue:
# 		oClient.ep.rpcRoleLogin(uResponse.iValue)
# 		addTimes(iId)
#  
# def rpcWalk(iDelay,oClient,iId):
# 	if not hasattr(oClient,'iX') or not hasattr(oClient,'iY') or not hasattr(oClient,'iRoleId'):
# 		bFail,uResponse=oClient.ep.rpcPos()
# 		if bFail:
# 			return
# 		iRoleId=uResponse.iRoleId
# 		iCurX=uResponse.iX
# 		iCurY=uResponse.iY
# 		iDir=0
# 		iHeadDir=3
# 		setXY(oClient,iCurX,iCurY,iRoleId,0,3)
# 	else:
# 		iRoleId=oClient.iRoleId
# 		iCurX=oClient.iX
# 		iCurY=oClient.iY
# 		iDir=oClient.iDir
# 		iHeadDir=oClient.iHeadDir
# 	iCurX,iCurY=bountXY(iCurX,iCurY)
#  
# 	iDstDir=random.randint(0,8)
# 	iFlip=1
# 	iState=1030
# 	if iDir==0:
# 		if iDstDir==0: 
# 			return
# 	else:
# 		if iDstDir==0:
# 			iState=1010
#  
# 	if iHeadDir==3:
# 		if iDstDir>5:
# 			iFlip=-1
# 			iHeadDir=7
# 	else:
# 		if iDstDir<=5:
# 			iFlip=-1
# 			iHeadDir=3
#  
# 	#--- dir ---
# 	msg=sync_pb2.syncMsg()
# 	msg.dir.iEttId=iRoleId
# 	msg.dir.iDir=iDstDir
# 	msg.dir.iCurX=iCurX
# 	msg.dir.iCurY=iCurY
# 	oClient.ep.rpcRoleSync(msg)
# 	addTimes(iId)
# 	#--- flip ---
# 	if iFlip==-1:
# 		msg=sync_pb2.syncMsg()
# 		msg.flip.iEttId=iRoleId
# 		msg.flip.iFlip=iFlip
# 		oClient.ep.rpcRoleSync(msg)
# 		addTimes(iId)
# 	#--- act ---
# 	msg=sync_pb2.syncMsg()
# 	msg.act.iEttId=iRoleId
# 	msg.act.iState=iState
# 	msg.act.iDir=iDstDir
# 	msg.act.iCurX=iCurX
# 	msg.act.iCurY=iCurY
# 	oClient.ep.rpcRoleSync(msg)
# 	addTimes(iId)
#  
# 	#--------disDir-------
# 	iSpeedX,iSpeedY=gdSpeed[iDstDir]
# 	iDstX=iCurX+iSpeedX*iDelay
# 	iDstY=iCurY+iSpeedY*iDelay
# 	iDstX,iDstY=bountXY(iDstX,iDstY)
#  
# 	setXY(oClient,int(iDstX),int(iDstY),iRoleId,iDir,iHeadDir)  #保存客户端的状态
#  
# def rpcTalk(iDelay,oClient,iId):
# 	msg=chatRoom_pb2.chatUplink()
# 	msg.iEndPoint=2
# 	msg.sContent='Hi,this is robot {}!'.format(iId)
# 	oClient.ep.rpcChat(msg)
# 	addTimes(iId)
#  
# def rpcSwitchMap(iDelay,oClient,iId):
# 	global gtSceneNoToSwitch
# 	i=random.randint(0,2)
# 	iSceneNo=gtSceneNoToSwitch[i]
# 	msg=common_pb2.int32_()
# 	msg.iValue=iSceneNo
# 	oClient.ep.rpcServerSwitchTown(msg)
# 	addTimes(iId)
#  
# if 'gdClient' not in globals():
# 	gdClient={}
# 	gsTest=set((1,2,3,4,5))
# 	gtSceneNoToSwitch=(10,11,12)
# 	iMinX,iMaxX=400,2300
# 	iMinY,iMaxY=20,280
#  
# def setXY(oClient,iX,iY,iRoleId,iDir,iHeadDir):
# 	oClient.iX=iX
# 	oClient.iY=iY
# 	oClient.iRoleId=iRoleId
# 	oClient.iDir=iDir
# 	oClient.iHeadDir=iHeadDir
#  
# def bountXY(iX,iY):
# 	if iX<=100:
# 		iX=100
# 	elif iX>=2300:
# 		iX=2300
# 	if iY<=44:
# 		iY=44
# 	elif iY>=297:
# 		iY=297
# 	return iX,iY
#  
# def addTimes(iId,bTime=True):
# 	lTimes=gdAmountAndTime.setdefault(iId,[])
# 	if not lTimes:
# 		lTimes.append(1)
# 		if bTime:
# 			lTimes.append(timeU.stamp2str())
# 	else:
# 		lTimes[0]=lTimes[0]+1
# 		if bTime:
# 			if len(lTimes)==2 :
# 				lTimes[1]=timeU.stamp2str()
# 			else:
# 				lTimes.append(timeU.stamp2str())
# 
# import gevent
# import misc
# import config
# import u
# import timer
# 
# import random
# import common_pb2
# import gevent.event
# import primitive
# import timeU
# import log
# import time
# 
# 
# gdSpeed={0:(0,0),1:(0,400),2:(320,340),3:(400,0),4:(320,-340),5:(0,-400),6:(-320,-340),7:(-400,0),8:(-320,340)}
# import config
# -*- coding: utf-8 -*-
import mainSvc
import terminal_main_pb2
import accountSvc
import account_pb2
import roleSvc
import role_pb2
import sceneSvc
import scene_pb2
import chatSvc
import terminal_chat_pb2
import terminal_scene_pb2

gtService = {
	"service":(
		mainSvc.cService,
		accountSvc.cService,
		roleSvc.cService,
		sceneSvc.cService,
		chatSvc.cService,
	),
	"stub":(
		terminal_main_pb2.terminal2main_Stub,
		account_pb2.terminal2main_Stub,
		role_pb2.terminal2main_Stub,
		scene_pb2.terminal2main_Stub,
		terminal_chat_pb2.terminal2chat_Stub,
		terminal_scene_pb2.terminal2scene_Stub,
	)
}


# 
# 
# class cService2(serviceMisc_pb2.gameClientMiscService):
# 	@endPoint.result
# 	def rpcSendBubble(self,ep,who,reqMsg):
# 		pass
# 
# class cService1(terminal_main_pb2.main2terminal):
# 	@endPoint.result
# 	def rpcAvatarAttrInit(self,ep,who,reqMsg):
# 		global iRoleId,iLv,iExp,sName
# 		iRoleId=reqMsg.iRoleId
# 		iLv=reqMsg.iLevel
# 		iExp=reqMsg.iExp
# 		sName=reqMsg.sName
# 
# 	@endPoint.result
# 	def rpcAvatarAttrChange(self,ep,who,reqMsg):
# 		global iLv,iExp
# 		if getattr(reqMsg,'iLv',0):
# 			iLv=reqMsg.iLevel
# 		if getattr(reqMsg,'iExp',0):
# 			iExp=reqMsg.iExp
# 
# 	@endPoint.result
# 	def rpcSendName(self,ep,oAccount,reqMsg):		
# 		# ep.rpcSetRoleName(reqMsg.iValue)
# 		iSchool=1#random.randint(1,2)
# 		bFail,uRespons=ep.rpcCreateRole(reqMsg.iValue,iSchool)
# 		if bFail:
# 			return
# 		if uRespons.iRoleId:
# 			ep.rpcRoleLogin(uRespons.iRoleId)
# 
# 	@endPoint.result
# 	def rpcSwitchScene(self,ep,who,reqMsg):
# 		return True
# 
# 	@endPoint.result
# 	def rpcRoleList(self,ep,ctrlr,reqMsg):
# 		oRole=None
# 		for oRole in reqMsg.roles:			
# 			print u.trans2gbk('Id：{}'.format(oRole.iRoleId))
# 		if oRole:
# 			ep.rpcRoleLogin(oRole.iRoleId)
# 		else:
# 			ep.rpcRandomName()
# 
# 	@endPoint.result
# 	def rpcAddPropsToPackage(self,ep,who,reqMsg):
# 		if reqMsg.iPropsId==10101 or reqMsg.iPropsId==10201:
# 			return
# 		ep.rpcClickButton(1,reqMsg.iPropsId) #穿上刚得到的装备
# 
# 	@endPoint.result
# 	def rpcConfirmBox(self,ep,who,reqMsg):
# 		return 0
# 
# 	@endPoint.result
# 	def rpcPushMailList(self,ep,who,reqMsg):#邮件列表
# 		ep.waiter.set()
# 		# global iLv
# 		# if iLv==1:
# 		# 	gainRandomExp(ep)	#得经验
# 			#getRanodmEquip(ep) #拿装备
# 			#joinLeague(ep)		#进联赛
# 		#randomRun(ep)		#随机跑
# 
# 	@endPoint.result	
# 	def rpcRequireSceneXY(self,ep,who,reqMsg):
# 		return (0, 0)
# 
# def randomRun(ep):
# 	iMinX,iMaxX=400,2300
# 	iMinY,iMaxY=20,280
# 			
# 	import sync_pb2
# 	while True:
# 		bFail,uResponse=ep.rpcPos()
# 		if bFail:
# 			return
# 		iRoleId=uResponse.iRoleId
# 		iCurX=uResponse.iX
# 		iCurY=uResponse.iY
# 		iDstX=random.randint(iMinX,iMaxX)
# 		iDstY=random.randint(iMinY,iMaxY)
# 		diffX=iDstX-iCurX
# 		diffY=iDstY-iCurY
# 		iFlip=1
# 		if diffX>0:
# 			if diffY>0:
# 				iDir=3
# 			elif diffY<0:
# 				iDir=5
# 			else:
# 				iDir=4
# 		elif diffX<0:
# 			iFlip=-1
# 			if diffY>0:
# 				iDir=9
# 			elif diffY<0:
# 				iDir=7
# 			else:
# 				iDir=8
# 		else:
# 			if diffY>0:
# 				iDir=2
# 			elif diffY<0:
# 				iDir=6
# 			else:
# 				iDir=1
# 		fSleepTime=(diffX**2+diffY**2)**0.5/313
# 		#--- start moving ---
# 		msg=sync_pb2.syncMsg()
# 		#--- act ---
# 		msg.act.iEttId=iRoleId
# 		msg.act.iState=1030
# 		msg.act.iDir=iDir
# 		msg.act.iCurX=iCurX
# 		msg.act.iCurY=iCurY
# 		#--- flip ---
# 		msg.flip.iEttId=iRoleId
# 		msg.flip.iFlip=iFlip
# 		#--- dir ---
# 		msg.dir.iEttId=iRoleId
# 		msg.dir.iDir=iDir
# 		msg.dir.iCurX=iCurX
# 		msg.dir.iCurY=iCurY
# 		ep.rpcRoleSync(msg)
# 		gevent.sleep(fSleepTime)
# 		#--- stop moving ---
# 		msg=sync_pb2.syncMsg()
# 		#--- dir ---
# 		msg.dir.iEttId=iRoleId
# 		msg.dir.iDir=1
# 		msg.dir.iCurX=iDstX
# 		msg.dir.iCurY=iDstY
# 		ep.rpcRoleSync(msg)
# 
# 		msg=sync_pb2.syncMsg()
# 		#--- act ---
# 		msg.act.iEttId=iRoleId
# 		msg.act.iState=1010
# 		msg.act.iDir=1
# 		msg.act.iCurX=iDstX
# 		msg.act.iCurY=iDstY
# 		ep.rpcRoleSync(msg)
# 		gevent.sleep(2)
# 
# def joinLeague(ep):
# 	ep.rpcServerLeague()
# 
# def gainRandomExp(ep):
# 	iExp=random.randint(200000,2000000000)
# 	ep.rpcInstruction('addExp {}'.format(iExp))
# 
# def getRanodmEquip(ep):
# 	global iLv
# 	iTempLv=iLv/10*10
# 	sHasGet=set()
# 	for iNo,dValue in equipData.gdData.iteritems():
# 		if dValue.get('等级')==iTempLv:
# 			if dValue.get('wearPos') not in sHasGet:
# 				sHasGet.add(dValue.get('wearPos'))
# 				ep.rpcInstruction('np {}'.format(iNo))
# 
# gRoleLoginSuccessful={}
# 
# import random
# import gevent
# 
# import c
# import u
# import equipData
# import props
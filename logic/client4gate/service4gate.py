#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import backEnd_gate_pb2
import endPoint
import misc
import config

class cService(backEnd_gate_pb2.gate2backEnd):
	@endPoint.result
	def rpcGameClientConnect(self,ep,ctrlr,reqMsg):return rpcGameClientConnect(self,ep,ctrlr,reqMsg)

	@endPoint.result
	def rpcGameClientDisConnected(self,ep,ctrlr,reqMsg):return rpcGameClientDisConnected(self,ep,ctrlr,reqMsg)

	@endPoint.result
	def rpcOtherBackEndLink2gate(self,ep,ctrlr,reqMsg):return rpcOtherBackEndLink2gate(self,ep,ctrlr,reqMsg)

	@endPoint.result
	def rpcRecoverySceneService(self,ep,ctrlr,reqMsg):return rpcRecoverySceneService(self,ep,ctrlr,reqMsg)

	@endPoint.result
	def rpcSwitchSceneResponse(self,ep,ctrlr,reqMsg):return rpcSwitchSceneResponse(self,ep,ctrlr,reqMsg)

def rpcOtherBackEndLink2gate(self,ep,ctrlr,reqMsg):#有其他backEnd连接到网关
	iReportBackEnd=reqMsg.iValue
	sBackEndName=backEnd.gdServiceName[iReportBackEnd]
	backEnd.backEndEvent.channelBuilt(iReportBackEnd,2)

def rpcGameClientDisConnected(self,ep,ctrlr,reqMsg):#有一个游戏客户端连接断开了与网关的连接,全关闭
	iConnId=reqMsg.iValue
	clientEP=None
	if 'mainService' in SYS_ARGV:
		clientEP=mainService.gEndPointKeeper.getObj(iConnId)

	if 'sceneService' in SYS_ARGV:
		clientEP=sceneService.gEndPointKeeper.getObj(iConnId)

	if 'chatService' in SYS_ARGV:
		clientEP=chatService.gEndPointKeeper.getObj(iConnId)

	if not clientEP:
		return
	sText='收到网关消息,有游戏客户端关闭了.网关编号={},connId={},ip={},port={}'.format(ep.gateServiceNo(),iConnId,clientEP.ip(),clientEP.port())
	print sText
	log.log('rpc4gate',sText)
	clientEP.recvClose()

def rpcGameClientConnect(self,ep,ctrlr,reqMsg):#有一个新的游戏客户端连接到网关了,网关发消息通到后端了
	iGateServiceId=reqMsg.iGateServiceId
	iConnId=reqMsg.iConnId #各个后端都用网关生成的id来标识一个连接
	sIP=reqMsg.sIP
	iPort=reqMsg.iPort
	
	sText='收到网关消息,游戏客户端连上来了,网关编号={},connId={},ip={},port={}'.format(iGateServiceId,iConnId,sIP,iPort)
	print sText
	log.log('rpc4gate',sText)

	bDebugMode=config.IS_INNER_SERVER
	if 'mainService' in SYS_ARGV:
		ep=mainService.playerEP.cMSplayerEP(bDebugMode,gdMainService)
		ep.setAssociativeGateServiceId(iGateServiceId)
		ep.setEndPointId(iConnId).setIP(sIP).setPort(iPort)	
		ep.start()
		mainService.gEndPointKeeper.addObj(ep,iConnId)


		gdeqRecentConnection.append('{} {}:{}'.format(timeU.stamp2str(),sIP,iPort))
		while len(gdeqRecentConnection)>20:#40
			gdeqRecentConnection.popleft()

	if 'sceneService' in SYS_ARGV:
		ep=sceneService.cPlayerEndPoint(bDebugMode,gdSceneService)
		
		ep.setEndPointId(iConnId).setIP(sIP).setPort(iPort)	
		ep.start()
		sceneService.gEndPointKeeper.addObj(ep,iConnId)

		gdeqRecentConnection4Scene.append('{} {}:{}'.format(timeU.stamp2str(),sIP,iPort))
		while len(gdeqRecentConnection4Scene)>20:#40
			gdeqRecentConnection4Scene.popleft()

	if 'chatService' in SYS_ARGV:
		ep=chatService.playerEP.cPlayerEndPoint(bDebugMode,gdChatService)
		#ep.setAssociativeGateServiceId(iGateServiceId)
		ep.setEndPointId(iConnId).setIP(sIP).setPort(iPort)	
		ep.start()
		chatService.gEndPointKeeper.addObj(ep,iConnId)

	return True

def rpcRecoverySceneService(self,ep,ctrlr,reqMsg):
	if 'mainService' in SYS_ARGV:
		scene.recoverySceneService()
	return True


def rpcSwitchSceneResponse(self,ep,ctrlr,reqMsg):
	if 'mainService' in SYS_ARGV:
		scene.SwitchSceneResponse(reqMsg.iValue)
	return True

import c
import timeU
import u
import log

import gateService
import chatService
import chatService.playerEP
import chatService.service4terminal
import terminal_chat_pb2

import mainService
import mainService.combineService
import terminal_main_pb2
import serviceMisc_pb2
import mainService.playerEP
import backEnd
import backEnd.backEndEvent
import backEnd_pb2

import sceneService
import sceneService.service4terminal
import terminal_scene_pb2
import svcAccount
import account_pb2
import scene
import scene.service
import scene_pb2

#import svcPackage
import props_pb2
import war.service
import war_pb2
import role.service
import role_pb2
import skill.service
import skill_pb2
import pet.service
import pet_pb2

import ride.service
import ride_pb2

import props.service
import props_pb2

import shop.service
import shop_pb2

import team.service
import team_pb2
import buddy.service
import buddy_pb2
import task.service
import task_pb2

import activity.service
import act_guaji_pb2
import act_center_pb2
import act_race_pb2
import act_teamRace_pb2
import act_escort_pb2
import act_guildFight_pb2
import act_treasure_pb2
import act_instance_pb2
import act_fairyland_pb2
import act_star_pb2

import lineup_pb2
import lineup.service
import money_pb2
import qanda.service
import qanda_pb2
import hyperlink.service
import hyperlink_pb2
import state.service
import state_pb2
import equipMake.service
import equipMake_pb2
import mail.service
import mail_pb2
import words_pb2
import words.service
import title_pb2
import title.service
import alchemy_pb2
import alchemy.service
import collect.service4terminal
import collect_pb2
import holiday.service
import holiday_pb2
import rank.service
import rank_pb2
import trade_pb2
import trade.service
import dye_pb2
import dye.service
import signIn_pb2
import signIn.service
import guild_pb2
import guild.service
import guide_pb2
import guide.service
import answer_pb2
import answer.service
import achv_pb2
import achv.service
import treasureShop_pb2
import treasureShop.service
import friend_pb2
import friend.service

gtSceneStub=(terminal_scene_pb2.scene2terminal_Stub,)
gtChatStub=(terminal_chat_pb2.chat2terminal_Stub,)
gtFightStub=()
gtMainStub=(
		terminal_main_pb2.main2terminal_Stub,
		serviceMisc_pb2.gameClientMiscService_Stub,
		account_pb2.main2terminal_Stub,
		scene_pb2.main2terminal_Stub,
		#svcPackage.cService,props_pb2.main2terminal_Stub,
		war_pb2.main2terminal_Stub,
		role_pb2.main2terminal_Stub,
		skill_pb2.main2terminal_Stub,
		pet_pb2.main2terminal_Stub,
		ride_pb2.main2terminal_Stub,
		props_pb2.main2terminal_Stub,
		shop_pb2.main2terminal_Stub,
		team_pb2.main2terminal_Stub,
		buddy_pb2.main2terminal_Stub,
		task_pb2.main2terminal_Stub,
		
		# 活动
		act_guaji_pb2.main2terminal_Stub,
		act_center_pb2.main2terminal_Stub,
		act_race_pb2.main2terminal_Stub,
		act_teamRace_pb2.main2terminal_Stub,
		act_escort_pb2.main2terminal_Stub,
		act_guildFight_pb2.main2terminal_Stub,
		act_treasure_pb2.main2terminal_Stub,
		act_instance_pb2.main2terminal_Stub,
		act_fairyland_pb2.main2terminal_Stub,
		act_star_pb2.main2terminal_Stub,
		
		lineup_pb2.main2terminal_Stub,
		money_pb2.main2terminal_Stub,
		qanda_pb2.main2terminal_Stub,
		hyperlink_pb2.main2terminal_Stub,
		state_pb2.main2terminal_Stub,
		equipMake_pb2.main2terminal_Stub,
		mail_pb2.main2terminal_Stub,
		words_pb2.main2terminal_Stub,
		title_pb2.main2terminal_Stub,
		words_pb2.main2terminal_Stub,
		alchemy_pb2.main2terminal_Stub,
		collect_pb2.main2terminal_Stub,
		holiday_pb2.main2terminal_Stub,
		rank_pb2.main2terminal_Stub,
		signIn_pb2.main2terminal_Stub,
		trade_pb2.main2terminal_Stub,
		dye_pb2.main2terminal_Stub,
		guild_pb2.main2terminal_Stub,
		guide_pb2.main2terminal_Stub,
		answer_pb2.main2terminal_Stub,
		achv_pb2.main2terminal_Stub,
		treasureShop_pb2.main2terminal_Stub,
		friend_pb2.main2terminal_Stub,
		)

gtAllStub=gtSceneStub+gtMainStub+gtChatStub+gtFightStub

#-----------------------------------------------------

gdSceneService={#场景服务
	'service':(sceneService.service4terminal.cService,),
	'stub':gtAllStub
}

gdChatService={#聊天服务
	'service':(chatService.service4terminal.cService,),
	'stub':gtAllStub
}

gdFightService={#战斗服务
	'service':(),
	'stub':gtAllStub
}

gdMainService={#主服务
	'service':(
		mainService.combineService.cService1,
		mainService.combineService.cService2,
		svcAccount.cService,
		war.service.cService,
		scene.service.cService,
		role.service.cService,
		skill.service.cService,
		pet.service.cService,
		ride.service.cService,
		props.service.cService,
		shop.service.cService,
		team.service.cService,
		buddy.service.cService,
		task.service.cService,
		
		# 活动
		activity.service.cServiceGuaji,
		activity.service.cServiceCenter,
		activity.service.cServicePk,
		activity.service.cServiceRace,
		activity.service.cServiceTeamRace,
		activity.service.cServiceEscort,
		activity.service.cServiceGuildFight,
		activity.service.cServiceTreasure,
		activity.service.cServiceInstance,
		activity.service.cServiceFairylandFight,
		activity.service.cServiceStar,

		lineup.service.cService,
		qanda.service.cService,
		hyperlink.service.cService,
		state.service.cService,
		equipMake.service.cService,
		mail.service.cService,
		words.service.cService,
		title.service.cService,
		alchemy.service.cService,
		collect.service4terminal.cService,
		holiday.service.cService,
		rank.service.cService,
		signIn.service.cService,
		trade.service.cService,
		dye.service.cService,
		guild.service.cService,
		guide.service.cService,
		answer.service.cService,
		achv.service.cService,
		treasureShop.service.cService,
		friend.service.cService,
		),

	'stub':gtAllStub
}


import collections

if 'gbOnce' not in globals():
	gbOnce=True

	gdeqRecentConnection=collections.deque()#双端队列,记录主服最近的连接信息

	gdeqRecentConnection4Scene=collections.deque()#双端队列,记录场景服最近的连接信息
#-*-coding:utf-8-*-

import collect_pb2
import endPoint

#客户端-->主服
class cService(collect_pb2.terminal2main):

	@endPoint.result
	def rpcCollectTest(self, ep, who, reqMsg): return rpcCollectTest(who, reqMsg)
	
	@endPoint.result
	def rpcCollectUpdateLocation(self, ep, who, reqMsg): return rpcCollectUpdateLocation(who, reqMsg)

	@endPoint.result
	def rpcCollectAround(self, ep, who, reqMsg): return rpcCollectAround(who, reqMsg)

	@endPoint.result
	def rpcCollectSearch(self, ep, who, reqMsg): return rpcCollectSearch(who, reqMsg)

	@endPoint.result
	def rpcCollectSeeTrigger(self, ep, who, reqMsg): return rpcCollectSeeTrigger(who, reqMsg)

	@endPoint.result
	def rpcCollectSelfTrigger(self, ep, who, reqMsg): return rpcCollectSelfTrigger(who, reqMsg)

	@endPoint.result
	def rpcCollectSeeMarker(self, ep, who, reqMsg): return rpcCollectSeeMarker(who, reqMsg)

	@endPoint.result
	def rpcCollectMarker(self, ep, who, reqMsg): return rpcCollectMarker(who, reqMsg)

	@endPoint.result
	def rpcCollectDelEvent(self, ep, who, reqMsg): return rpcCollectDelEvent(who, reqMsg)

	@endPoint.result
	def rpcCollectFight(self, ep, who, reqMsg): return rpcCollectFight(who, reqMsg)

	@endPoint.result
	def rpcCollectEnter(self, ep, who, reqMsg): return rpcCollectEnter(who, reqMsg)

	@endPoint.result
	def rpcCollectGreet(self, ep, who, reqMsg): return rpcCollectGreet(who, reqMsg)

	@endPoint.result
	def rpcCollectAddFriend(self, ep, who, reqMsg): return rpcCollectAddFriend(who, reqMsg)

def rpcCollectTest(who, reqMsg):
	# print "=====rpcCollectTest:客户端-->主服协议"
	oCenterEP = client4center.getCenterEndPoint()
	oCenterEP.rpcMainCollectTest()

def rpcCollectEnter(who, reqMsg):
	'''进入退出收集玩法
	'''
	iValue = reqMsg.iValue
	setattr(who, "enterCollect", iValue)
	if iValue:
		who.denyTeam["collect_go"] = "收集玩法"
	else:
		who.denyTeam.pop("collect_go", None)
		#退出收集玩法
		team.platformservice.playerAutoMatch(who)

def rpcCollectUpdateLocation(who, reqMsg):
	'''更新位置信息，用于查找周围玩家
	'''
	# collect.CollectLog("rpcCollectUpdateLocation id={}".format(who.id))
	oCenterEP = client4center.getCenterEndPoint()
	msg = {}
	msg["iRoleId"] = who.id
	msg["iServerId"] = config.ZONE_NO
	msg["fPosX"] = reqMsg.fPosX
	msg["fPosY"] = reqMsg.fPosY
	msg["iGender"] = who.gender
	msg["sName"] = who.name
	msg["iSchool"] = who.school
	
	oCenterEP.rpcB2CCollectUpdateLocation(**msg)
	
def rpcCollectAround(who, reqMsg):
	'''周围玩家
	'''
	# collect.CollectLog("rpcCollectAround id={}".format(who.id))
	oCenterEP = client4center.getCenterEndPoint()

	msg = {}
	msg["iRoleId"] = who.id
	msg["iServerId"] = config.ZONE_NO
	msg["fPosX"] = reqMsg.fPosX
	msg["fPosY"] = reqMsg.fPosY
	pid = who.id
	bFail, resMsg = oCenterEP.rpcB2CCollectAround(**msg)
	who = getRole(pid)
	if not who:
		return
	if bFail:
		return
	if resMsg.sFailReason:
		message.tips(who, resMsg.sFailReason)
	who.send(resMsg.sAroundRole)


def rpcCollectFight(who, reqMsg):
	'''进入战斗
	'''
	if who.inWar():
		message.tips(who, "战斗中不能触发事件")
		return
	if who.week.fetch("OCFight", 0) >= 15:
		message.tips(who, "#C04本周剩余次数为0#n，无法进入战斗")
		return
	#todo 询问中心服可不可以
	oCenterEP = client4center.getCenterEndPoint()
	iEventId = reqMsg.iEventId
	msg = {}
	msg["iEventId"] = iEventId
	msg["iRoleId"] = who.id
	msg["iServerId"] = config.ZONE_NO
	msg["iGender"] = who.gender
	msg["sName"] = who.name
	msg["fPosX"] = reqMsg.fPosX
	msg["fPosY"] = reqMsg.fPosY
	
	pid = who.id
	bFail,resMsg = oCenterEP.rpcB2CCollectTriggerEvent(**msg)
	if bFail:
		return
	if resMsg.sFailReason:
		message.tips(who, resMsg.sFailReason)
		return
	who = getRole(pid)
	if not who:
		return
	gameObj = collect.getMainCollectObj()
	#进入战斗
	iEventNo = resMsg.iEventNo
	iFightIdx = gameObj.getFightIdx(iEventNo)
	warObj = gameObj.fight(who, None, iFightIdx)
	if warObj:
		who.week.add("OCFight", 1)
		rpcCollectLeftCount(who)
		gameObj.setEventArgs(who.id, iEventNo, msg)
		who.addHandlerForWarEnd("CollectFight_%s"%who.id, gameObj.delEventNo)

def rpcB2CCollectWarWin(msg):
	'''通知中心服，战斗胜利
	'''
	oCenterEP = client4center.getCenterEndPoint()
	oCenterEP.rpcB2CCollectWarWin(**msg)

def rpcCollectSearch(who, reqMsg):
	'''搜索
	'''
	# collect.CollectLog("rpcCollectSearch id={}".format(who.id))
	oCenterEP = client4center.getCenterEndPoint()
	msg = {}
	msg["iRoleId"] = who.id
	msg["iServerId"] = config.ZONE_NO
	msg["fPosX"] = reqMsg.fPosX
	msg["fPosY"] = reqMsg.fPosY
	msg["iGender"] = who.gender
	msg["sName"] = who.name
	msg["iSchool"] = who.school

	pid = who.id
	bFail, resMsg = oCenterEP.rpcB2CCollectSearch(**msg)
	who = getRole(pid)
	if not who:
		return
	if not bFail:
		who.send(resMsg.sValue)

def rpcCollectSeeMarker(who, reqMsg):
	'''查看标记事件
	'''
	# collect.CollectLog("rpcCollectSeeMarker id={}".format(who.id))
	oCenterEP = client4center.getCenterEndPoint()
	pid = who.id
	bFail,resMsg = oCenterEP.rpcB2CCollectSeeMarker(pid)
	if bFail:
		return
	who = getRole(pid)
	if not who:
		return
	if not bFail:
		who.send(resMsg.sValue)

def rpcCollectSelfTrigger(who, reqMsg):
	'''查看完成
	'''
	# collect.CollectLog("rpcCollectSelfTrigger id={}".format(who.id))
	oCenterEP = client4center.getCenterEndPoint()
	pid = who.id
	bFail,resMsg = oCenterEP.rpcB2CCollectSelfTrigger(pid)
	if bFail:
		return
	who = getRole(pid)
	if not who:
		return
	if not bFail:
		who.send(resMsg.sValue)

def rpcCollectSeeTrigger(who, reqMsg):
	'''查看触发
	'''
	# collect.CollectLog("rpcCollectSeeTrigger id={}".format(who.id))
	oCenterEP = client4center.getCenterEndPoint()
	pid = who.id
	bFail,resMsg = oCenterEP.rpcB2CCollectSeeTrigger(pid)
	if bFail:
		return
	who = getRole(pid)
	if not who:
		return
	if not bFail:
		who.send(resMsg.sValue)

def rpcCollectMarker(who, reqMsg):
	'''标记事件
	'''
	# collect.CollectLog("rpcCollectMarker id={}".format(who.id))
	msg = {}
	msg["iRoleId"] = who.id
	msg["iEventId"] = reqMsg.iEventId
	oCenterEP = client4center.getCenterEndPoint()
	pid = who.id
	bFail,resMsg = oCenterEP.rpcB2CCollectMarker(**msg)
	if bFail:
		return
	who = getRole(pid)
	if not who:
		return
	if resMsg.sTips:
		message.tips(who, resMsg.sTips)
	if resMsg.sSerialized:
		who.send(resMsg.sSerialized)

def rpcCollectDelEvent(who, reqMsg):
	'''删除事件
	'''
	# collect.CollectLog("rpcCollectDelEvent id={}".format(who.id))
	msg = {}
	msg["iRoleId"] = who.id
	msg["iEventId"] = reqMsg.iEventId
	msg["iEventType"] = reqMsg.iEventType
	oCenterEP = client4center.getCenterEndPoint()
	pid = who.id
	bFail,resMsg = oCenterEP.rpcB2CCollectDelEvent(**msg)
	if bFail:
		return
	who = getRole(pid)
	if not who:
		return
	if bFail:
		return
	if resMsg.sTips:
		message.tips(who, resMsg.sTips)
	if resMsg.sSerialized:
		who.send(resMsg.sSerialized)

def sendDelEvent(who, iEventId, iEventType):
	msg = {}
	msg["iEventId"] = iEventId
	msg["iEventType"] = iEventType
	who.endPoint.rpcCollectDelEventResponse(**msg)

def rpcCollectLeftCount(who):
	'''剩余次数
	'''
	count = max(0, 15-who.week.fetch("OCFight", 0))
	who.endPoint.rpcCollectLeftCount(count)

def rpcCollectGreet(who, reqMsg):
	'''打招呼
	'''
	# print "======rpcCollectGreet==1234123==="
	iGreetRoleId = reqMsg.iValue
	if iGreetRoleId == who.id:
		return

	iCurSecond = getSecond()
	dCollectGreet = who.fetch("collectGreet", {})
	#超过时间的删除掉
	lTemp = []
	iCoolTime = 12*3600	#12小时
	for iGreetRoleId,iTime in dCollectGreet.iteritems():
		if iCurSecond > iTime + iCoolTime:
			lTemp.append(iGreetRoleId)

	if lTemp:
		for iGreetRoleId in lTemp:
			dCollectGreet.pop(iGreetRoleId, None)
		who.set("collectGreet", dCollectGreet)

	if iGreetRoleId in dCollectGreet:
		if dCollectGreet.get(iGreetRoleId, 0) + iCoolTime >= iCurSecond:
			message.tips(who, '你已向对方提出打过招呼了，太频繁小心吓到对方哦')
			return

	dCollectGreet[iGreetRoleId] = iCurSecond
	who.set("collectGreet", dCollectGreet)
	message.tips(who, '你向对方热情地打了一声招呼，对方似乎听到了……')
	# print "=======rpcCollectGreet====",who.id,iGreetRoleId
	friend.sendMsg(who, iGreetRoleId, '我掐指一算，竟然和阁下毗邻，加个好友一起玩吧')

	
def rpcCollectAddFriend(who, reqMsg):
	'''加为好友
	'''
	# print "======rpcCollectAddFriend==1234123==="
	iFriendId = reqMsg.iRoleId
	iEventType = reqMsg.iEventType
	iEventNo = reqMsg.iEventNo
	if iFriendId == who.id:
		message.tips(who, '自己加自己好友，真是寂寞如雪啊……')
		return

	# if iEventType not in (COMPLETE_EVENT, TRIGGER_EVENT):
	# 	return

	friend.add(who, iFriendId)
	# print "=======rpcCollectAddFriend====",who.id,iFriendId,iEventType,iEventNo
	mainOutCollectObj = collect.getMainCollectObj()
	sEventName = mainOutCollectObj.getEventName(iEventNo)
	sContent = ''
	if iEventType == COMPLETE_EVENT:
		sContent = '茫茫人海，我竟有幸获得阁下遗留的#C02{}#n，让我们加个好友吧'.format(sEventName)

	elif iEventType == TRIGGER_EVENT:
		sContent = '哈哈哈，想不到我遗失的#C02{}#n竟然有幸被阁下获得，这么有缘，加个好友一起玩吧'.format(sEventName)

	if sContent:
		friend.sendMsg(who, iFriendId, sContent)


from common import *
from collect.defines import *
import log
import c
import u
import misc
import role
import backEnd
import client4center
import collect
import message
import config
import team.platformservice
import friend
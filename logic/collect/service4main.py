#-*-coding:utf-8-*-

import center_collect_pb2
import endPoint
import misc

#主服-->中心服
class cService(center_collect_pb2.backEnd2center):
	@endPoint.result
	def rpcMainCollectTest(self,ep,ctrlr,reqMsg): return rpcMainCollectTest(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectUpdateLocation(self,ep,ctrlr,reqMsg): return rpcB2CCollectUpdateLocation(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectSearch(self,ep,ctrlr,reqMsg): return rpcB2CCollectSearch(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectTriggerEvent(self,ep,ctrlr,reqMsg): return rpcB2CCollectTriggerEvent(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectWarWin(self,ep,ctrlr,reqMsg): return rpcB2CCollectWarWin(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectSeeTrigger(self,ep,ctrlr,reqMsg): return rpcB2CCollectSeeTrigger(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectSelfTrigger(self,ep,ctrlr,reqMsg): return rpcB2CCollectSelfTrigger(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectSeeMarker(self,ep,ctrlr,reqMsg): return rpcB2CCollectSeeMarker(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectMarker(self,ep,ctrlr,reqMsg): return rpcB2CCollectMarker(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectDelEvent(self,ep,ctrlr,reqMsg): return rpcB2CCollectDelEvent(ctrlr,reqMsg)

	@endPoint.result
	def rpcB2CCollectAround(self,ep,ctrlr,reqMsg): return rpcB2CCollectAround(ctrlr,reqMsg)


#=====================================================
#=====================================================
def rpcMainCollectTest(ctrlr,reqMsg):
	# print "rpcMainCollectTest:主服-->中心服协议",ctrlr
	# ctrlr.rpcCenterCollectTest()

	if reqMsg.iType == 1:
		return newSpecialEvent(reqMsg)
	elif reqMsg.iType == 2:
		return clearSpecialEvent(reqMsg)
	return ""

giOneKm = 250#1000
giTwoKm = 500#2000
def newSpecialEvent(reqMsg):
	'''生成指定事件
	'''
	iRoleId = reqMsg.iRoleId
	iEventCnt = reqMsg.iEventCnt
	iAngle = reqMsg.iAngle
	iDistance = reqMsg.iDistance

	mainOutCollectObj = collect.getMainCollectObj()
	lEventNoKeys = mainOutCollectObj.getShufferEventNoList()
	if not lEventNoKeys:
		raise Exception,"室外收集玩法，战斗表为空"

	roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
	if not roleInfoObj:
		return

	gCenterCollectObj = collect.getCenterCollectObj()
	iServerId = roleInfoObj.iServerId
	sName = roleInfoObj.sName
	iGender = roleInfoObj.iGender
	fPosX,fPosY = roleInfoObj.getLocationInfo()
	# print "newSpecialEvent fPosX,fPosY",fPosX,fPosY,iAngle,iDistance
	index = 0
	iTotal = len(lEventNoKeys)-1
	lEventList = []
	for i in xrange(iEventCnt):
		iEventNo = lEventNoKeys[index]
		fLatitude, fLongitude = collect.getRandLatAndLongitude(fPosX, fPosY, 1, giOneKm, iAngle, iDistance)
		# print "==========fLatitude, fLongitude=",fLatitude, fLongitude
		iEventId = gCenterCollectObj.newEventInfo(iEventNo, iRoleId, iServerId, sName, iGender, fLatitude, fLongitude)
		lEventList.append(iEventId)
		index += 1
		if index >= iTotal:
			index = 0
	roleInfoObj.addProductEventList(lEventList)
	roleInfoObj.setLastSearch(lEventList)
	roleInfoObj.setSpecialEvent(lEventList)
	# print "======newSpecialEvent========",lEventList
	# lEventMsg = []
	# for iEventId in lEventList:
	# 	eventInfoObj = gCenterCollectObj.getEventInfoObj(iEventId)
	# 	if not eventInfoObj:
	# 		continue
	# 	lEventMsg.append(packetEvent(iEventId, eventInfoObj))
	# msg = collect_pb2.eventList()
	# msg.eventType = 1
	# msg.lEventList.extend(lEventMsg)
	# return endPoint.makePacket('rpcCollectEventList', msg)

def clearSpecialEvent(reqMsg):
	iRoleId = reqMsg.iRoleId
	roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
	if not roleInfoObj:
		return
	roleInfoObj.setSpecialEvent([])
#=====================================================
#=====================================================

def rpcB2CCollectUpdateLocation(ctrlr, reqMsg):
	'''更新位置信息，用于查找周围玩家
	'''
	# collect.CollectLog("rpcB2CCollectUpdateLocation id={}".format(reqMsg.iRoleId))
	roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(reqMsg.iRoleId)
	roleInfoObj.updateRoleInfo(reqMsg)

def packetAroundRoleInfo(roleInfoObj):
	msg = collect_pb2.roleInfo()
	msg.iRoleId = roleInfoObj.iRoleId
	msg.iServerId = roleInfoObj.iServerId
	msg.fPosX = "%.6f"%(roleInfoObj.fPosX)
	msg.fPosY = "%.6f"%(roleInfoObj.fPosY)
	msg.sPicture = roleInfoObj.sPicture
	msg.iGender = roleInfoObj.iGender
	msg.sName = roleInfoObj.sName
	msg.iSchool = roleInfoObj.iSchool
	msg.sServerName = misc.zoneName()	#临时的
	return msg

def rpcB2CCollectAround(ctrlr, reqMsg):
	lAroundRoleId = collect.gRoleInfoMngObj.getAroundRole(reqMsg.iRoleId, reqMsg.iServerId, float(reqMsg.fPosX), float(reqMsg.fPosY))
	msg = center_collect_pb2.aroundRoleResponse()
	roleListMsg = collect_pb2.roleList()
	if not lAroundRoleId:
		msg.sFailReason = "很遗憾，本地区还有玩家未开启定位功能"
		# msg.sAroundRole = ""
	else:
		msg.sFailReason = ""
		lRoleMsg = []
		for iRoleId in lAroundRoleId:
			roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
			if not roleInfoObj:
				continue
			lRoleMsg.append(packetAroundRoleInfo(roleInfoObj))
		roleListMsg.lRoleList.extend(lRoleMsg)
	msg.sAroundRole = endPoint.makePacket('rpcAroundRoleInfo', roleListMsg)
	return msg

def rpcB2CCollectTriggerEvent(ctrlr, reqMsg):
	'''进入战斗
	'''
	gCenterCollectObj = collect.getCenterCollectObj()
	iEventNo,sFailReason = gCenterCollectObj.triggerEvent(reqMsg)
	msg = center_collect_pb2.triggerEventRes()
	msg.iEventNo = iEventNo
	msg.sFailReason = sFailReason
	return msg

def rpcB2CCollectWarWin(ctrlr,reqMsg):
	'''战斗胜利
	'''
	gCenterCollectObj = collect.getCenterCollectObj()
	gCenterCollectObj.warWin(reqMsg)


def packetEvent(iEventId, eventInfoObj):
	msg = collect_pb2.eventInfo()
	msg.iEventId = iEventId
	msg.iEventNo = eventInfoObj.iEventNo
	msg.iServerId = eventInfoObj.iServerId
	msg.fPosX = "%.6f"%(eventInfoObj.fPosX)
	msg.fPosY = "%.6f"%(eventInfoObj.fPosY)
	msg.iTimeOut = eventInfoObj.iEndTime
	msg.iSchool = eventInfoObj.iSchool
	msg.sServerName = misc.zoneName()	#临时的
	#print "===========afasdfsfsad"
	return msg

def rpcB2CCollectSearch(ctrlr, reqMsg):
	'''搜索
	'''
	# collect.CollectLog("rpcB2CCollectSearch id={}".format(reqMsg.iRoleId))
	iRoleId = reqMsg.iRoleId
	roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
	gCenterCollectObj = collect.getCenterCollectObj()
	lEventList = roleInfoObj.getSpecialEvent()
	if not lEventList:
		lEventList = gCenterCollectObj.searchEvent(reqMsg)
	lEventMsg = []
	
	for iEventId in lEventList:
		eventInfoObj = gCenterCollectObj.getEventInfoObj(iEventId)
		if not eventInfoObj:
			continue
		lEventMsg.append(packetEvent(iEventId, eventInfoObj))
	msg = collect_pb2.eventList()
	msg.eventType = SEARCH_EVENT
	msg.lEventList.extend(lEventMsg)
	return endPoint.makePacket('rpcCollectEventList', msg)

def packetMarkerEvent(dEventInfo):
	msg = collect_pb2.eventInfo()
	iEventId = dEventInfo.get("iEventId", 0)
	msg.iEventId = iEventId
	msg.iEventNo = dEventInfo.get("iEventNo", 0)
	msg.iServerId = dEventInfo.get("iServerId", 0)
	msg.sName = dEventInfo.get("sName", "")
	msg.sPicture = dEventInfo.get("sPicture", "")
	msg.fPosX = "%.6f"%(dEventInfo.get("fPosX", 0))
	msg.fPosY = "%.6f"%(dEventInfo.get("fPosY", 0))
	msg.iSchool = dEventInfo.get("iSchool", 11)
	msg.sServerName = misc.zoneName()	#临时的

	gCenterCollectObj = collect.getCenterCollectObj()
	eventObj = gCenterCollectObj.getEventInfoObj(iEventId)
	msg.iTimeOut = eventObj.iEndTime if eventObj else getSecond()
	return msg

def rpcB2CCollectSeeMarker(ctrlr, reqMsg):
	'''查看标记事件
	'''
	iRoleId = reqMsg.iRoleId
	roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
	lMarkerEvent = roleInfoObj.getMarkerEvent()
	lEventMsg = []
	for dEventInfo in lMarkerEvent:
		lEventMsg.append(packetMarkerEvent(dEventInfo))

	msg = collect_pb2.eventList()
	msg.eventType = MARKER_EVENT
	msg.lEventList.extend(lEventMsg)
	return endPoint.makePacket('rpcCollectEventList', msg)


def packetComEvent(dEventInfo):
	msg = collect_pb2.eventInfo()
	msg.iEventId = dEventInfo.get("iEventId", 0)
	msg.iEventNo = dEventInfo.get("iEventNo", 0)
	msg.iServerId = dEventInfo.get("iServerId", 0)
	msg.sName = dEventInfo.get("sName", "")
	msg.iDistance = int(dEventInfo.get("iDistance", 0))
	msg.sPicture = dEventInfo.get("sPicture", "")
	msg.iComTime = dEventInfo.get("iComTime", 0)
	msg.iGender = dEventInfo.get("iGender", 0)
	msg.iSchool = dEventInfo.get("iSchool", 11)
	msg.iRoleId = dEventInfo.get("iRoleId", 0)
	msg.sServerName = misc.zoneName()	#临时的
	return msg

def rpcB2CCollectSelfTrigger(ctrlr, reqMsg):
	'''查看完成
	'''
	iRoleId = reqMsg.iRoleId
	roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
	lComEvent = roleInfoObj.getCompleteEvent()
	lEventMsg = []
	for dEventInfo in lComEvent:
		lEventMsg.append(packetComEvent(dEventInfo))

	msg = collect_pb2.eventList()
	msg.eventType = COMPLETE_EVENT
	msg.lEventList.extend(lEventMsg)
	return endPoint.makePacket('rpcCollectEventList', msg)

def packetRoleInfo(dRoleInfo):
	msg = collect_pb2.eventInfo()
	msg.iEventId = dRoleInfo.get("iLastId", 0)#dRoleInfo.get("iEventId", 0)
	msg.iEventNo = dRoleInfo.get("iEventNo", 0)
	msg.iServerId = dRoleInfo.get("iServerId", 0)
	msg.sName = dRoleInfo.get("sName", "")
	msg.iDistance = int(dRoleInfo.get("iDistance", 0))
	msg.sPicture = dRoleInfo.get("sPicture", "")
	msg.iComTime = dRoleInfo.get("iComTime", 0)
	msg.iGender = dRoleInfo.get("iGender", 0)
	msg.iSchool = dRoleInfo.get("iSchool", 11)
	msg.iRoleId = dRoleInfo.get("iRoleId", 0)
	msg.sServerName = misc.zoneName()	#临时的
	return msg

def rpcB2CCollectSeeTrigger(ctrlr, reqMsg):
	'''查看触发
	'''
	iRoleId = reqMsg.iRoleId
	roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
	lRoleInfo = roleInfoObj.getTriggerRoleInfo()
	lEventMsg = []
	for dRoleInfo in lRoleInfo:
		lEventMsg.append(packetRoleInfo(dRoleInfo))
	
	msg = collect_pb2.eventList()
	msg.eventType = TRIGGER_EVENT
	msg.lEventList.extend(lEventMsg)
	return endPoint.makePacket('rpcCollectEventList', msg)

def rpcB2CCollectMarker(ctrlr,reqMsg):
	'''标记事件
	'''
	iRoleId = reqMsg.iRoleId
	iEventId = reqMsg.iEventId
	roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)

	resMsg = center_collect_pb2.eventOperResponse()

	gCenterCollectObj = collect.getCenterCollectObj()
	eventObj = gCenterCollectObj.getEventInfoObj(iEventId)
	if not eventObj or not eventObj.isValid():
		resMsg.sTips = "标志消失，事件已消失"
	elif roleInfoObj.isMarkerEvent(iEventId):
		resMsg.sTips = "事件已标记"
	else:
		resMsg.sTips = "成功标记事件#C04{}#n".format(eventObj.eventName())
		dEventInfo = roleInfoObj.markerEvent(eventObj)
		msg = collect_pb2.eventList()
		msg.eventType = MARKER_EVENT
		msg.lEventList.extend([packetMarkerEvent(dEventInfo)])
		resMsg.sSerialized = endPoint.makePacket("rpcCollectAddEvent", msg)
	
	return resMsg

def rpcB2CCollectDelEvent(ctrlr,reqMsg):
	iRoleId = reqMsg.iRoleId
	iEventId = reqMsg.iEventId
	iEventType = reqMsg.iEventType
	roleInfoObj = collect.gRoleInfoMngObj.getRoleInfoObj(iRoleId)
	result = False
	resMsg = center_collect_pb2.eventOperResponse()
	if iEventType == MARKER_EVENT:	#标记
		result,iEventNo = roleInfoObj.removeMarkerEvent(iEventId)
		if result:
			mainOutCollectObj = collect.getMainCollectObj()
			resMsg.sTips = "取消对#C04{}#n的标记".format(mainOutCollectObj.getEventName(iEventNo))
	elif iEventType == COMPLETE_EVENT:#完成
		result = roleInfoObj.removeCompleteEvent(iEventId)
		if result:
			resMsg.sTips = "删除成功"
	elif iEventType == TRIGGER_EVENT:#触发
		result = roleInfoObj.removeTriggerInfo(iEventId)
		if result:
			resMsg.sTips = "删除成功"
	if result:
		msg = collect_pb2.delEventInfo()
		msg.iEventId = iEventId
		msg.iEventType = iEventType
		resMsg.sSerialized = endPoint.makePacket('rpcCollectDelEventResponse', msg)
	return resMsg

def getCenterEP(iZoneNo):
	# print "====getCenterEP=======",iZoneNo, backEnd_pb2.MAIN_SERVICE
	# print centerService.cs4backEnd.gBackEndProxy.dProxy
	return centerService.cs4backEnd.gBackEndProxy.getProxy((iZoneNo, backEnd_pb2.MAIN_SERVICE))

def rpcC2BCollectAddEvent(iEventType, eventObj, proRoleInfoObj, roleInfoObj=None):
	'''增加事件
	'''
	iZoneNo = proRoleInfoObj.iServerId
	oCenterEP = getCenterEP(iZoneNo)
	if not oCenterEP:
		return

	msg = center_collect_pb2.passiveEventInfo()
	msg.iRoleId = proRoleInfoObj.iRoleId

	addmsg = collect_pb2.eventList()
	addmsg.eventType = iEventType

	if iEventType == MARKER_EVENT:	#标记
		addmsg.lEventList.extend([packetMarkerEvent(eventObj.packetData())])
	elif iEventType == COMPLETE_EVENT:#完成
		addmsg.lEventList.extend([packetComEvent(eventObj.packetData())])
	elif iEventType == TRIGGER_EVENT:#触发
		addmsg.lEventList.extend([packetRoleInfo(roleInfoObj.packetData())])

	msg.sSerialized = endPoint.makePacket("rpcCollectAddEvent", addmsg)
	oCenterEP.rpcC2BCollectAddEvent(msg)

def rpcC2BCollectDelEvent(iZoneNo, iRoleId, iEventId, iEventType):
	'''删除事件
	'''
	iZoneNo = roleInfoObj.iServerId
	oCenterEP = getCenterEP(iZoneNo)
	if not oCenterEP:
		return
	msg = center_collect_pb2.passiveEventInfo()
	msg.iRoleId = iRoleId

	delmsg = collect_pb2.delEventInfo()
	delmsg.iEventId = iEventId
	delmsg.iEventType = iEventType

	msg.sSerialized = endPoint.makePacket("rpcCollectDelEventResponse", delmsg)

	oCenterEP.rpcC2BCollectDelEvent(msg)

from common import *
import log
import c
import u
import misc
import role
import backEnd
import client4center
import collect
from collect.defines import *
import collect_pb2
import endPoint
import centerService.cs4backEnd
import backEnd_pb2
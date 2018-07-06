# -*- coding: utf-8 -*-
'''节日礼物服务
'''
import endPoint
import holiday_pb2

class cService(holiday_pb2.terminal2main):
	
	@endPoint.result
	def rpcHolidayTake(self, ep, who, reqMsg): return rpcHolidayTake(who, reqMsg)

def rpcHolidayTake(who, reqMsg):
	'''领取节日礼物
	'''
	holidayId = holidayData.getCurrentHoliday()#reqMsg.holidayId
	if holiday.isTakeGift(who, holidayId): # 已领取
		return
	if not holidayId or holidayId != holidayData.getCurrentHoliday(): # 不是当前节日或当前没有节日
		message.tips(who,"已经过去了，下个节日也有大礼哦")
		rpcHolidayUI(who)
		return
	
	levelLimit = holidayData.getConfig(holidayId, "领取等级")
	if who.level < levelLimit:
		return

	rewardData = holidayData.getConfig(holidayId, "奖励")
	if not who.propsCtn.validCapacity(rewardData):
		message.tips(who, "包裹已满，请清理包裹才能领取节日礼物")
		return

	holiday.markTakeGift(who, holidayId)
	rpcHolidayChange(who, holidayId, "isTaken")
	writeLog("holiday/take", "%d %d" % (who.id, holidayId))
	
	for propsNo, amount in rewardData.iteritems():
		launch.launchBySpecify(who, propsNo, amount, False, "节日礼物")

	task.removeTask(who,10001)
	message.tips(who,"你领取了节日大奖")

#===============================================================================
# 服务端发往客户端
#===============================================================================
def packetStateMsg(who, holidayId):
	'''节日状态
	'''
	isTaken = holiday.isTakeGift(who, holidayId)

	msgObj = holiday_pb2.stateMsg()
	msgObj.holidayId = holidayId
	msgObj.isTaken = isTaken
	return msgObj

def packetUIMsg(who):
	'''节日礼物界面信息
	'''
	holidayId = holidayData.getCurrentHoliday()
	if holidayId:
		stateMsgObj = packetStateMsg(who, holidayId)
	else:
		stateMsgObj = None
	
	msgObj = holiday_pb2.UIMsg()
	if stateMsgObj:
		msgObj.currentHoliday.CopyFrom(stateMsgObj)
	msgObj.currentTime = getSecond()
	return msgObj

def rpcHolidayUI(who):
	'''打开节日礼物界面
	'''
	msgObj = packetUIMsg(who)
	who.endPoint.rpcHolidayUI(msgObj)

def rpcHolidayChange(who, holidayId, *attrNameList):
	'''改变节日状态
	'''
	msg = {"holidayId": holidayId}
	for attrName in attrNameList:
		if attrName == "isTaken":
			isTaken = holiday.isTakeGift(who, holidayId)
			msg[attrName] = isTaken
			
	who.endPoint.rpcHolidayChange(**msg)


from common import *
import holidayData
import holiday
import message
import launch
import task
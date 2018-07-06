# -*- coding: utf-8 -*-
# 坐骑服务
import endPoint
import ride_pb2

def handleLock(oldFunc):
	def newFunc(self,ep,who,reqMsg):
		import role.roleConfig
		if role.roleConfig.isLock(who):
			who.endPoint.rpcSecurityUnlock()
			return
		try:
			return oldFunc(self,ep,who,reqMsg)
		except Exception:
			raise
	return newFunc

class cService(ride_pb2.terminal2main):
	@endPoint.result
	def rpcRideBuyPoint(self, ep, who, reqMsg): return rpcRideBuyPoint(who, reqMsg)

	@endPoint.result
	def rpcRideCurrent(self, ep, who, reqMsg): return rpcRideCurrent(who, reqMsg)

	@endPoint.result
	def rpcRideBuy(self, ep, who, reqMsg): return rpcRideBuy(who, reqMsg)

	@endPoint.result
	def rpcRideHatchComplete(self, ep, who, reqMsg): return rpcRideHatchComplete(who, reqMsg)

	@endPoint.result
	def rpcRideHatchStart(self, ep, who, reqMsg): return rpcRideHatchStart(who, reqMsg)

	@endPoint.result
	def rpcRideGetListData(self, ep, who, reqMsg): return rpcRideGetListData(who, reqMsg)


def rpcRideBuyPoint(who, reqMsg):
	'''购买点数
	'''
	poindData = rideData.getBuyPointInfo(reqMsg.iValue)

	if not money.checkTradeCash(who,poindData[0]):#who.tradeCash < poindData[0]:
		# message.tips(who, "元宝不足")#这里改成了弹出兑换框
   		return
   	message.tips(who,"购买成功，你已增加#R<{},11,2>#n点骑乘体力！".format(poindData[1]))
   	who.costTradeCash(poindData[0],"骑乘体力",None)
   	who.rideCtn.addPoint(poindData[1])

def rpcRideCurrent(who,reqMsg):
	'''坐骑使用或休息
	'''
	rideId = reqMsg.rideId
	rideCurrent = reqMsg.rideCurrent
	rideObj = checkRide(who, rideId)
	if not rideObj:
 		return
	if rideCurrent:#坐
		who.rideCtn.setRideCurrent(rideObj, True)
	else:#不坐
		who.rideCtn.setRideCurrent(rideObj, False)
		message.tips(who, "你已解除坐骑骑乘！")
	pass

def rpcRideBuy(who, reqMsg):
	'''购买坐骑
	'''
	print "买坐骑--------",reqMsg,reqMsg.iValue
	pass

def rpcRideHatchComplete(who, reqMsg):
	'''直接完成孵化
	'''
	rideId = reqMsg.iValue
	rideObj = checkRide(who, rideId)
	if not rideObj:
		return
	if rideObj.idx == 6001:
		message.tips(who, "祭炼结束方可骑乘坐骑，请耐心等待")
		return
	#弹出提示框
	timeOut = rideObj.hatchTimeOut - getSecond()
	if 0 >= timeOut:
		return
	cash = 1 + timeOut / rideData.getConfig("加速孵化消耗")
	msg = '''坐骑#C06{}#n离祭炼完成还有#C07{}#n，是否花费#R<{},102,2>#n直接完成祭炼？
Q取消
Q确定'''.format(rideObj.name,timeU.getTimeStr(timeOut),cash)
	message.confirmBoxNew(who,functor(rideHatchComplete,rideId),msg)

def rideHatchComplete(who,buyComplete,rideId):
	if not buyComplete:
		return
	rideObj = checkRide(who, rideId)
	if not rideObj:
		return
	timeOut = rideObj.hatchTimeOut - getSecond()
	if 0 >= timeOut:
		return
	cash = 1 + timeOut / rideData.getConfig("加速孵化消耗")
	if not money.checkTradeCash(who,cash):
		# message.tips(who, "元宝不足")#这里改成了弹出兑换框
   		return
   	who.costTradeCash(cash,"加速孵化",None)
	nextRide = rideData.getData(rideObj.idx,"下一只坐骑")
	who.stopTimer("rideHatchComplete")
	rideObj.rideHatchComplete(nextRide)


def rpcRideHatchStart(who,reqMsg):
	'''开始孵化
	'''
	rideId = reqMsg.iValue
	rideObj = checkRide(who, rideId)
	if not rideObj:
		return
	if rideObj.state != ride.object.RIDE_EGG:
		message.tips(who, "坐骑已开始祭炼")
		return
	message.tips(who,"你的坐骑#C06{}#n已开始祭炼，请耐心等待吧！".format(rideObj.name))
	rideObj.rideHatchStart(who)

	pass

def rpcRideGetListData(who,reqMsg):
	rpcRideList(who)

def checkRide(who, rideId):
	'''检查异兽是否存在
	'''
	rideObj = who.rideCtn.getItem(rideId)
	if not rideObj:
		message.tips(who, "该坐骑不存在")
		return None
	return rideObj

def getRide(who,rideIdx):
	for rideObj in who.rideCtn.getAllValues():
		if rideObj.idx == rideIdx:
			return rideObj
	return None

def rpcRideList(who):
	'''发送坐骑列表
	'''
	rideListMsg = ride_pb2.rideListMsg()
	rideListMsg.rideMsgList.extend(getrideDataList(who))
	rideListMsg.point = who.rideCtn.ridePoint
	rideListMsg.maxPoint = rideData.getConfig("骑乘点上限")
	who.endPoint.rpcRideList(rideListMsg)

def getrideDataList(who):
	rideDataList = []
	rideidx = []
	for rideObj in who.rideCtn.getAllValues():#拥有的坐骑
		rideidx.append(rideObj.idx)
		rideDataList.append(packRideData(rideObj))
	for rideId in rideData.rideData.keys():#没有的坐骑
		if rideId in rideidx:
			continue
		rideObj = ride.new(rideId)
		rideDataList.append(packRideData(rideObj))
	return rideDataList


def rpcRideAdd(who, rideObj):
	'''增加坐骑
	'''
	rideConfig = packRideData(rideObj)
	who.endPoint.rpcRideAdd(rideConfig)
	

def packRideData(rideObj):
	timeOut = 0
	if rideObj.hatchTimeOut:
		timeOut = max(0, rideObj.hatchTimeOut - getSecond())

	rideMsg = ride_pb2.rideMsg()

	rideMsg.rideId = rideObj.id
	rideMsg.rideNo = rideObj.idx
	rideMsg.shape = rideObj.shape
	rideMsg.shapeParts.extend(rideObj.shapeParts)
	rideMsg.colors.extend(rideObj.getColors())
	rideMsg.state = rideObj.state
	rideMsg.timeOut = timeOut
	rideMsg.isNewRide = rideObj.isNewRide()
	return rideMsg

from common import *
import message
import rideData
import ride
import ride.object
import role
import u
import timeU
import money
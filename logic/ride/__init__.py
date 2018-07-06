#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#坐骑基类

def new(idx=6001):
	rideObj = ride.object.Ride()
	rideObj.set("idx", idx)
	data = rideData.getData(idx)
	rideObj.onBorn(data)
	return rideObj

def createAndLoad(data):
	obj = ride.object.Ride()
	obj.load(data)
	#obj.reCalcAttr(False)
	return obj
	
def addRide(who, rideObj,state=1):
	'''增加坐骑
	'''
	rideObj.state = state
	who.rideCtn.addItem(rideObj)
	return rideObj

def getRideName(idx):
	'''获取坐骑原始名称
 	'''
	data = rideData.getData(idx)
	if data:
		return data["名称"]
	return "坐骑%s" % idx

def rideMountStart(who):
	rideObj = who.rideCtn.getRindCurrent()
	if not rideObj:
		raise "玩家没上坐骑不应该到这里来"
		return
	who.rideCtn.rideCurrentTime = getSecond()
	lastTimeOut = who.rideCtn.rideTimeOut
	timeOut = rideData.getConfig("坐骑点扣除周期")
	point = rideObj.getConfig("点数消耗")
	anima = rideObj.getConfig("灵力")
	if 0 >= lastTimeOut:
		lastTimeOut = timeOut
		who.rideCtn.rideTimeOut = timeOut
	if not who.eDisConnected.contain(disMount):
		who.eDisConnected+=disMount
	who.startTimer(functor(ride.rideMountLoop,who.id,timeOut,point,anima),lastTimeOut, "rideMountLoop")


def rideMountLoop(roleId, timeOut, point, anima):
	who=getRole(roleId)
	if not who:
		return
	who.rideCtn.addPoint(-point, "坐骑周期性扣除")
	who.alchemyCtn.addAnima(anima)#增加灵气
	who.rideCtn.rideCurrentTime = getSecond()
	who.rideCtn.rideTimeOut = timeOut
	who.rideCtn.markDirty()
	if point > who.rideCtn.ridePoint:
		message.tips(who, "你的骑乘体力不足，骑乘状态已解除")
		who.rideCtn.setRideCurrent(who.rideCtn.getRindCurrent(), False)
		return
	who.endPoint.rpcAnimaMod(who.alchemyCtn.getAnima())
	who.startTimer(functor(ride.rideMountLoop,who.id,timeOut,point,anima),timeOut, "rideMountLoop")
	
def disMount(who):
	if who.eDisConnected.contain(disMount):
		who.eDisConnected-=disMount
	who.stopTimer("rideMountLoop")
	who.rideCtn.rideTimeOut -= getSecond()-who.rideCtn.rideCurrentTime

	who.rideCtn.markDirty()

def updateRideList(who):
	rideObjList = []
	for rideObj in who.rideCtn.getAllValues():
		if ride.object.RIDE_MATCH == rideObj.state:
			rideObjList.append(rideObj)
	for rideObj in rideObjList:
		rideObj.rideHatchStart(who,True)

def isride(who):
	if who.rideCtn.getRindCurrent():
		rideMountStart(who)

def onUpLevel(who):
	if who.level == rideData.getConfig("开放等级"):
		rideObj = new(6001)
		addRide(who,rideObj)

from common import *
import ride.object
import u
import c
import rideData
import message
import datetime

# -*- coding: utf-8 -*-
import pst
RIDE_NO_NULOCK=0
RIDE_EGG=1
RIDE_MATCH=2
RIDE_REST=3
RIDE_USE=4
class Ride(pst.cEasyPersist):
	def __init__(self):
		pst.cEasyPersist.__init__(self)
		self.id = 0
		self.ownerId = 0
		self.hatchTimeOut = 0
		self.state = 0

	def onBorn(self, data):  # override
		self.id = block.sysActive.gActive.genRideId()
		self.set("name", data["名称"])
		self.set("timeOut", 0)
		self.set("birthday", timeU.getDayNo())

	def getConfig(self, key):
		return rideData.getData(self.idx, key)

	@property
	def key(self):
		return self.id

	@property
	def name(self):
		name = self.fetch("name")
		if not name:
			name = ride.getRideName(self.idx)
		return name

	@property
	def shape(self):
		'''造型
		'''
		shape = self.fetch("shape")
		if not shape:
			shape = self.getConfig("造型")
			shape,_ = template.transShapeStr(shape)
		return shape
	
	@property
	def shapeParts(self):
		'''造型部位
		'''
		shapeParts = self.fetch("shapeParts", {})
		return role.defines.transToShapePartListForRide(shapeParts)

	def getColors(self):
		'''染色
		'''
		colors = self.fetch("colors", {})
		return role.defines.transToColorListForRide(colors)

	def setColors(self, colorList):
		'''设置染色
		'''
		colors = self.fetch("colors", {})
		for shapePartType, color in colorList.items():
			colors[shapePartType] = color
		self.set("colors", colors)
		self.attrChange()
		who = self.getOwnerObj()
		if who and who.rideCtn.getRindCurrent():
			who.attrChange("rideShape", "rideShapePart", "rideColors")

	@property
	def idx(self):
		'''导表索引
		'''
		return self.fetch("idx", 6001)
	
	def getOwnerObj(self):
		return getRole(self.ownerId)

	def rideHatchStart(self,who,roleLand=False):#开始孵化
		if RIDE_EGG == self.state:
			timeOutData = rideData.getData(self.idx,"孵化时间")
			self.state = RIDE_MATCH
			self.hatchTimeOut = getSecond()+timeOutData*60*60
			self.markDirty()
			self.attrChange()#改变属性
		elif RIDE_MATCH != self.state:
			return
		timeOut =  self.hatchTimeOut - getSecond()
		nextRide = rideData.getData(self.idx,"下一只坐骑")
		if 0 < timeOut:#开始倒数 
			if not who.eDisConnected.contain(rideHatchTimeOutStop):
				who.eDisConnected += rideHatchTimeOutStop
			who.startTimer(functor(self.rideHatchComplete,nextRide),timeOut, "rideHatchComplete")
		else:
			self.rideHatchComplete(nextRide,roleLand)

	def rideHatchComplete(self,nextRide,roleLand=False):#孵化完成
		who=getRole(self.ownerId)
		if not who:
			return
		self.state = RIDE_REST
		#发放下一只坐骑
		if nextRide:
			rideObj = ride.new(nextRide)
			if rideObj:
				ride.addRide(who, rideObj)
			rideObj.attrChange()
		if not roleLand:
			self.attrChange()
		self.markDirty()
		title = "{}完成祭炼！".format(self.name)
		if self.idx == 6001:
			giftPoint = rideData.getConfig("首只孵化奖励")
			who.rideCtn.addPoint(giftPoint)
			msg = "你的坐骑#C06{}#n完成了祭炼并给予了你#C02{}#n点骑乘体力，快骑上坐骑遨游一番吧！".format(self.name,giftPoint)
		else:
			msg = "你的坐骑#C06{}#n已完成祭炼，快骑上坐骑遨游一番吧！".format(self.name)
		message.tips(who, msg)
		mail.sendSysMail(who.id, title, msg)
		if who.eDisConnected.contain(rideHatchTimeOutStop):
			who.eDisConnected -= rideHatchTimeOutStop

	def save(self):  # override
		dData = pst.cEasyPersist.save(self)
		dData["id"] = self.id
		dData["state"] = self.state
		dData["hatchTimeOut"] = self.hatchTimeOut
		return dData

	def load(self, dData):  # override
		pst.cEasyPersist.load(self, dData)
		self.id = dData.pop("id", 0)
		self.state = dData.pop("state", 0)
		self.hatchTimeOut = dData.pop("hatchTimeOut", 0)

	def attrChange(self):
		'''刷新属性
		'''
		who = self.getOwnerObj()
		msg = {"rideId": self.id,"rideNo": self.idx}
		attrNameList = ("shape","shapeParts","colors","state","rideCurrent","timeOut","isNewRide")
		for attrName in attrNameList:
			msg[attrName] = self.getValByName(attrName)
		if who:
			who.endPoint.rpcRideChange(**msg)
			
	def getValByName(self, attrName):
		'''根据属性名获取属性值
		'''
		return getValByName(self, attrName)

	def getTimeOut(self):
		timeOut = self.hatchTimeOut - getSecond()
		if timeOut >= 0:
			return timeOut
		return 0

	def isNewRide(self):
		if RIDE_REST != self.state or self.fetch("used"):
			return False
		return True

def rideHatchTimeOutStop(who):
	who.stopTimer("rideHatchComplete")
	if who.eDisConnected.contain(rideHatchTimeOutStop):
		who.eDisConnected -= rideHatchTimeOutStop

from common import *
import role.defines
import timeU
import block.sysActive
import ride
import rideData
import message
import template
import mail
import u
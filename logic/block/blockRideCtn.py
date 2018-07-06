# -*- coding: utf-8 -*-
import ctn
import block

class cRideContainer(ctn.cContainerBase,block.cCtnBlock):
	def __init__(self, iOwnerId):
		block.cCtnBlock.__init__(self,'坐骑容器',iOwnerId)
		ctn.cContainerBase.__init__(self,iOwnerId)
		self.setIsStm(sql.RIDE_CTN_INSERT)
		self.setDlStm(sql.RIDE_CTN_DELETE)
		self.setUdStm(sql.RIDE_CTN_UPDATE)
		self.setSlStm(sql.RIDE_CTN_SELECT)

		self.rideList = [] # 携带的坐骑
		self.rideCurrent = 0 # 正在使用的坐骑
		self.ridePoint = 0 # 骑乘体力
		self.rideTimeOut = 0 # 剩余倒数时间
	
	def _dirtyEventHandler(self):#override
		factoryConcrete.rideCtnFtr.schedule2tail4save(self.ownerId)

	def save(self):#override
		dData=ctn.cContainerBase.save(self)
		dData["rideList"] = self.rideList
		dData["rideCurrent"] = self.rideCurrent
		dData["ridePoint"] = self.ridePoint
		dData["rideTimeOut"] = self.rideTimeOut
		return dData
	
	def load(self,dData):#override  
		ctn.cContainerBase.load(self,dData)
		self.rideList = dData.pop("rideList", [])
		self.rideCurrent = dData.pop("rideCurrent", 0)
		self.ridePoint = dData.pop("ridePoint", 0)
		self.rideTimeOut = dData.pop("rideTimeOut", 0)

	def _createAndLoadItem(self,iIndex,uData):#override
		idx, dData = uData
		return ride.createAndLoad(dData)
	
	def _saveItem(self,iIndex,obj):#override
		return obj.idx, obj.save()

	def _rpcAddItem(self,obj):#override
		who = self.getOwnerObj()
		ride.service.rpcRideAdd(who, obj)
	
	def _rpcRemoveItem(self,obj):#override
		pass

	def _rpcRefresh(self):
		who = self.getOwnerObj()
		ride.updateRideList(who)
		ride.service.rpcRideList(who)

	def setRideCurrent(self, rideObj, isRideCurrent,replaceRide=True):
		rideId = rideObj.id
		who=getRole(self.ownerId)
		if isRideCurrent:
			if rideId == self.rideCurrent:
				return
			if self.rideCurrent: # 把旧坐的骑取消
				oldRideCurrent = self.getItem(self.rideCurrent)
				if oldRideCurrent:
					self.setRideCurrent(oldRideCurrent, False,False)
			if self.ridePoint < rideObj.getConfig("点数消耗"):
				message.tips(who, "你的骑乘体力不足，无法骑乘坐骑！")
				return
			self.rideCurrent = rideId
			rideObj.state = ride.object.RIDE_USE
			if not rideObj.fetch("used"):
				rideObj.set("used",1)
			rideObj.attrChange()
			ride.rideMountStart(who)
			who.attrChange('rideShape','rideShapePart','rideColors')
		else:
			if rideId != self.rideCurrent:
				return
			self.rideCurrent = 0
			rideObj.state = ride.object.RIDE_REST
			rideObj.attrChange()
			ride.disMount(who)
			if replaceRide:
				who.attrChange('rideShape')
		self.markDirty()
		
	def addPoint(self, addpoind,sReason=""):
		who=getRole(self.ownerId)
		maxPoind = rideData.getConfig("骑乘点上限")
		if self.ridePoint + addpoind > maxPoind:
			self.ridePoint = maxPoind
		elif 0 > self.ridePoint + addpoind:
			self.ridePoint = 0
			message.tips(who, "骑乘体力不能被扣至负数")
		else:
			self.ridePoint += addpoind
		who.endPoint.rpcRidePointChange(self.ridePoint)
		self.markDirty()
		writeLog("ride/point", "%d %d%+d->%d %s" % (self.ownerId, self.ridePoint, addpoind, self.ridePoint + addpoind, sReason))

	def getRindCurrent(self):
		'''获取正在坐的坐骑
		'''
		if self.rideCurrent:
			return self.getItem(self.rideCurrent)
		return None

from common import *
import sql
import factoryConcrete
import c
import u
import pet
import ride_pb2
import props
import log
import role
import ride.service
import ride.object
import rideData
import message
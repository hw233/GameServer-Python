# -*- coding: utf-8 -*-

class cContainer(object):
	'''经验状态容器
	'''

	def __init__(self, ownerId):
		self.ownerId = ownerId
		self.stateList = {}

	@property
	def endPoint(self):
	    return mainService.getEndPointByRoleId(self.ownerId)

	def getOwnerObj(self):
		return getRole(self.ownerId)

	def addItem(self, stateId):
		if stateId in self.stateList:
			return
		stateObj = state.new(stateId)
		self.stateList[stateId] = stateObj
		stateObj.ownerId = self.ownerId
		self.setup(stateObj)
		self._rpcAddItem(stateObj)

	def getItem(self,stateId):
		return self.stateList.get(stateId,None)

	def removeItem(self,stateId):
		if stateId not in self.stateList:
			return None
		stateObj = self.stateList.pop(stateId)
		self.cancelSetup(stateObj)
		self._rpcRemoveItem(stateObj)

	def updateItem(self,stateId):
		stateObj = self.getItem(stateId)
		if stateObj:
			self.endPoint.rpcStateInfo(stateObj.getMsg())

	def setup(self,stateObj):
		who = self.getOwnerObj()
		if who and hasattr(stateObj,"setup"):
			stateObj.setup(who)

	def cancelSetup(self, stateObj):
		who = self.getOwnerObj()
		if who and hasattr(stateObj, "cancelSetup"):
			stateObj.cancelSetup(who)

	def _rpcAddItem(self, stateObj):
		self.endPoint.rpcStateInfo(stateObj.getMsg())

	def _rpcRemoveItem(self, stateObj):
		self.endPoint.rpcStateInfoDel(stateObj.no)

from common import *
import mainService	
import state
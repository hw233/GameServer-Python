# -*- coding: utf-8 -*-
import pst
import block
import sql

class Offline(block.cBlock, pst.cEasyPersist):
	'''离线玩家对象
	'''

	def __init__(self, roleId):
		pst.cEasyPersist.__init__(self, self.__dirtyEventHandler)
		block.cBlock.__init__(self, '离线玩家数据', roleId)
		
		self.setIsStm(sql.OFFLINE_INSERT)
		self.setDlStm(sql.OFFLINE_DELETE)
		self.setUdStm(sql.OFFLINE_UPDATE)
		self.setSlStm(sql.OFFLINE_SELECT)
		
		self.id = roleId
		self.handlerList = [] # 处理函数

	def __dirtyEventHandler(self):
		import factoryConcrete
		factoryConcrete.offlineFtr.schedule2tail4save(self.id)
		
	def load(self, data):
		if not data:
			return

		pst.cEasyPersist.load(self, data["data"])
		self.handlerList = data["handlerList"]
	
	def save(self):
		data = {}
		data["data"] = pst.cEasyPersist.save(self)
		data["handlerList"] = self.handlerList
		return data
	
	def addHandler(self, handlerName, **kwargs):
		'''增加处理函数
		'''
		self.handlerList.append((handlerName, kwargs))
		self.markDirty()
		
	def executeHandler(self, who):
		'''上线执行处理函数
		'''
		handlerList = self.handlerList
		self.handlerList = []
		self.markDirty()

		for handlerName, kwargs in handlerList:
			handler = gHandlerList[handlerName]
			try:
				handler(who, **kwargs)
			except:
				logException()
			

from common import *
from offlineHandler.defines import *
	
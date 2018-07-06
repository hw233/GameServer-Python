# -*- coding: utf-8 -*-
import ctn
import block

class TeamTaskContainer(object):
	
	def __init__(self, ownerId):
		self.ownerId = ownerId
		self.list = {}
		
	def getTeam(self):
		return team.getTeam(self.ownerId)
	
	def itemCount(self):
		return len(self.list)
	
	def addItem(self, taskObj):
		taskId = taskObj.id
		if taskId in self.list:
			raise Exception("已有任务:%s" % taskId)
		self.list[taskObj.id]= taskObj
		self.setup(taskObj)
		self._rpcAddItem(taskObj)
		
	def setup(self, taskObj):
		teamObj = self.getTeam()
		taskObj.team = teamObj
		who = getRole(teamObj.leader)
		taskObj.setup(who)
		
	def getItem(self, taskId):
		return self.list.get(taskId)
		
	def removeItem(self, taskObj):
		taskObj.release()
		taskId = taskObj.id
		if taskId in self.list:
			del self.list[taskId]
		self._rpcRemoveItem(taskObj)
	
	def getAllKeys(self):
		return self.list.iterkeys()
	
	def getAllItems(self):
		return self.list.iteritem()
	
	def getAllValues(self):
		return self.list.itervalues()

	def _rpcAddItem(self, taskObj):
		for who in taskObj.getRoleList():
			task.service.rpcTaskAdd(who, taskObj)

	def _rpcRemoveItem(self, taskObj):
		for who in taskObj.getRoleList():
			task.service.rpcTaskDel(who, taskObj)
		
	def _rpcRefresh(self):
		for taskObj in self.list.itervalues():
			self._rpcAddItem(taskObj)
			
	def clearAll(self):
		taskList = self.list.values()
		for taskObj in taskList:
			self.removeItem(taskObj)

	def rpcRefresh(self, who):
		for taskObj in self.list.itervalues():
			task.service.rpcTaskAdd(who, taskObj)

from common import *
import u
import task
import task.service
import team
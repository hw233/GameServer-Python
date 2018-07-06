# -*- coding: utf-8 -*-
from achv.defines import *
import pst

class Achievement(pst.cEasyPersist):
	'''成就
	'''
	
	kind = ACHV_KIND_COMMON # 成就类型
	id = 0 # 成就编号
	name = "未知成就"
	point = 0 # 成就点
	hidden = False # 是否隐藏
	totalProgress = 0 # 总进度
	conditionList = {} # 条件列表
	eventList = () # 成就达成后触发的事件
	timeLimit = 0 # 时间限制
	
	def __init__(self):
		pst.cEasyPersist.__init__(self)
		self.ownerId = 0
	
	@property
	def key(self):
		return self.id
	
	def setDone(self):
		'''设置完成
		'''
		self.set("done", 1)
		self.set("doneTime", getSecond())#达成时间
		who = getRole(self.ownerId)
		if who:
			who.addAchvPoint(self.point, self.name)
		self.triggerEvent(who)
		achv.service.rpcAchvDone(who, self)

	def isDone(self):
		'''是否已完成
		'''
		if self.fetch("done"):
			return 1
		return 0
			
# 	def addProgress(self, val):
# 		'''增加进度
# 		'''
# 		self.add("progress", val)
# 		if self.fetch("progress") >= self.totalProgress: # 完成
# 			self.setDone()
# 		else:
# 			pass
# 			# toDo 刷新进度
			
	def addProgress(self, val):
		'''增加进度
		'''
		if self.isBreak(): # 中断了
			self.add("progressTmp", val)
			if self.fetch("progressTmp") > self.fetch("progress"):
				val = self.fetch("progressTmp") - self.fetch("progress")
				self.setBreak(False)
				self.delete("progressTmp")
			else:
				return

		self.add("progress", val)
		if self.fetch("progress") >= self.totalProgress: # 完成
			self.set("progress", self.totalProgress)
			self.setDone()
		else:
			who = getRole(self.ownerId)
			if who:
				achv.service.rpcAchvChangeProg(who, self)
				
	def addProgressForTimeLimit(self, val):
		'''增加有时间限制的进度
		'''
		beginTime = self.fetch("beginTime")
		if not beginTime:
			beginTime = getSecond()
			self.set("beginTime", beginTime)
	
		if getSecond() <= beginTime + self.timeLimit:
			self.addProgress(val)
			return

		beginTimeTmp = self.fetch("beginTimeTmp")
		if beginTimeTmp:
			if getSecond() > beginTimeTmp + self.timeLimit:
				self.set("beginTimeTmp", getSecond())
		else:
			self.set("beginTimeTmp", getSecond())
			self.setBreak(True)

		self.addProgress(val)
		if not self.isBreak():
			self.set("beginTime", self.fetch("beginTimeTmp"))
			self.delete("beginTimeTmp")
				
	def tryAddProgress(self, val):
		'''尝试增加进度
		'''
		if self.kind != ACHV_KIND_PROG:
			return
		if self.timeLimit:
			self.addProgressForTimeLimit(val)
		else:
			self.addProgress(val)
			
	def setBreak(self, isBreak):
		'''设置是否中断进度
		'''
		if isBreak:
			self.set("break", 1)
		else:
			self.delete("break")
		
	def isBreak(self):
		'''是否已中断进度
		'''
		if self.fetch("break"):
			return True
		return False
			
	def doneCondition(self, conditionVal):
		'''达成条件
		'''
		if self.kind != ACHV_KIND_COND:
			return

		condDoneList = self.fetch("condDoneList", {})
		for conditionNo, val in self.conditionList.iteritems():
			if conditionNo in condDoneList:
				continue
			if conditionVal != val:
				continue
			condDoneList[conditionNo] = 1
			self.set("condDoneList", condDoneList)
			if condDoneList.keys() == self.conditionList.keys(): # 完成
				self.setDone()
			else:
				who = getRole(self.ownerId)
				if who:
					achv.service.rpcAchvChangeCond(who, self)
			break
	
	def triggerEvent(self, who):
		'''触发事件
		'''
		import listener.defines
		for eventStr in self.eventList:
			if eventStr.startswith("$"): # 自定义的事件
				eventName = eventStr[1:]
				self.triggerCustomEvent(who, eventName)
			else:
				listener.defines.triggerEvent(who, eventStr)
		
	def triggerCustomEvent(self, who, eventName):
		'''触发自定义事件
		'''
		pass



from common import *
import achv.service

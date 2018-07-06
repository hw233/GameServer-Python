# -*- coding: utf-8 -*-
# 状态基类
import pst


class State(pst.cEasyPersist):
	def __init__(self):
		pst.cEasyPersist.__init__(self)
		self.ownerId=0
		self.timerMgr = timer.cTimerMng()

	def getOwnerObj(self):
		return getRole(self.ownerId)

	@property
	def key(self):
		return self.no

	def setup(self,who):
		ti = self.getTime()
		if ti is not None:
			if ti > 0:
				self.timerMgr.run(self.timeOut, ti, 0, "timeOut")
			else:
				self.timeOut()

	def setTime(self, ti):
		self.set("end", getSecond() + ti)

	def getTime(self):
		if self.fetch("end"):
			return max(0, self.fetch("end") - getSecond())
		return None

	def timeOut(self):
		'''超时
		'''
		if self.timerMgr.hasTimerId("timeOut"):
			self.timerMgr.cancel("timeOut")
		who = self.getOwnerObj()
		state.removeState(who, self.no)
		if hasattr(self, "onTimeOut"):
			self.onTimeOut()

	def onTimeout(self):#超时时间到
		pass

	def isValid(self):
		if self.getTime() == 0:
			return 0
		return 1

	def getMsg(self):
		sDesc = self.getInfo()
		iTime = self.getTime()
		
		msg=state_pb2.stateInfo()
		msg.iNo=self.no
		if sDesc is not None:
			msg.sDesc=sDesc
		if iTime is not None:
			msg.iTime=iTime
		return msg

	def getInfo(self):
		if self.info:
			return self.info
		return None


from common import *
import state_pb2
import timer
import state

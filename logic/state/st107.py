# -*- coding: utf-8 -*-
from state.object import State as customState

#导表开始
class State(customState):
	no= 107
	name = "入世修行传说"
	info = "入世修行传说：#C03$time#n"
#导表结束

	def getInfo(self):
		surplus = 1200
		owner = getRole(self.ownerId)
		if owner:
			taskObj = task.hasTask(owner, 30601)
			ti = taskObj.getTime()
			if not ti:
				ti = 0
			surplus = "剩余{}分钟".format(ti/60)
		info = self.info.replace("$time", surplus)
		return info

	def setup(self,who):
		ti = self.getTime()
		if ti is not None:
			if ti > 0:
				self.timerMgr.run(functor(self.checkTimeOut, who.id), 0, 60, "timeOut")
			else:
				self.timeOut()

	def checkTimeOut(self, pid):
		'''超时
		'''
		ti = self.getTime()
		if ti is not None:
			if ti > 0:
				who = getRole(pid)
				if who:
					who.stateCtn.updateItemByKey(107)
			else:
				self.timeOut()


from common import *
import task

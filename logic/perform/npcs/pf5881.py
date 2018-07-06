# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5881
	name = "驯兽师"
	configInfo = {
		"次数":1,
	}
#导表结束

	def onSetup(self, w):
		self.side = w.side
		w.war.addFunc("onAddWarrior", self.onAddWarrior)
		
	def onAddWarrior(self, w):
		if w.side != self.side:
			return
		if not w.isRole():
			return
		
		roleObj = getRole(w.getPID())
		if not roleObj:
			return
		teamObj = roleObj.inTeam()
		if teamObj and not teamObj.isLeader(roleObj.id): # 不是队长
			return
		
		self.addApply(w, "召唤次数", self.configInfo["次数"])
		
		
from common import *

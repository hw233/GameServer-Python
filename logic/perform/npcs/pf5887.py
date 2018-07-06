# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5887
	name = "冲击"
	configInfo = {
		"物理伤害结果加成":5,
		"法术伤害结果加成":5,
	}
#导表结束

	def onSetup(self, w):
		self.side = w.side
		w.war.addFunc("onAddWarrior", self.onAddWarrior)
		
	def onAddWarrior(self, w):
		if w.side != self.side:
			return
		for attrName, attrVal in self.configInfo.iteritems():
			self.addApply(w, attrName, attrVal)

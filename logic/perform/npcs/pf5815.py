# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5815
	name = "指挥强力"
	configInfo = {
		"物理伤害结果加成":3,
		"法术伤害结果加成":3,
	}
#导表结束

	def onSetup(self, w):
		self.side = w.side
		w.war.addFunc("onAddWarrior", self.onAddWarrior)
		
	def onAddWarrior(self, w):
		if w.side != self.side:
			return
		if not (w.isPet() or w.isBuddy()):
			return
		for attrName, attrVal in self.configInfo.iteritems():
			self.addApply(w, attrName, attrVal)

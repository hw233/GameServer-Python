# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5814
	name = "指挥加速"
	configInfo = {
		"速度加成":3,
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

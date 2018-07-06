# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5884
	name = "符师"
	configInfo = {
		"符能":5,
	}
#导表结束

	def onSetup(self, w):
		self.side = w.side
		w.war.addFunc("onAddWarrior", self.onAddWarrior)
		
	def onAddWarrior(self, w):
		if w.side != self.side:
			return
		w.addFuWen(self.configInfo["符能"])
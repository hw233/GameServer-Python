# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5609
	name = "白骨锁魂"
	configInfo = {
		"回复生命":10,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onPerform", self.onPerform)
		
	def onPerform(self, att, vicCast, attackType):
		if att.isDead():
			return
		hp = att.hpMax * self.configInfo["回复生命"] / 100
		att.addHP(hp, att)
	
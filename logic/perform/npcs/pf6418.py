# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6418
	name = "分身强制扣1血"
	configInfo = {
		"伤害":1,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAbsorb", self.onAbsorb)
		
	def onAbsorb(self, att, vic, dp, attackType):
		return self.configInfo["伤害"]
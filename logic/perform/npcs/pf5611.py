# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5611
	name = "化血宝刀"
	configInfo = {
		"生命值限制":50,
	}
#导表结束

	def onSetup(self, w):
		self.setApply(w, "PF1512_HPLimit", self.configInfo["生命值限制"])
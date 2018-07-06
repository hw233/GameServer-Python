# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5618
	name = "道法相济"
	configInfo = {
		"概率":20,
		"生命":50,
	}
#导表结束

	def onSetup(self, w):
		self.setApply(w, "PF5618Info", self.configInfo)
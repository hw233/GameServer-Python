# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5634
	name = "赤身教徒"
	configInfo = {
		"概率":10,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onCalTargetCount1421", self.onCalTargetCount)
		
	def onCalTargetCount(self, att, targetCount):
		if rand(100) < self.configInfo["概率"]:
			return targetCount + 1
		return targetCount
	
	
from common import *

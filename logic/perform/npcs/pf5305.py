# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5305
	name = "振翅扶摇"
	configInfo = {
		"增加目标数":1,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onCalTargetCount", self.onCalTargetCount)
		
	def onCalTargetCount(self, att, performObj, targetCount):
		if performObj.isMultiTarget():
			return self.configInfo["增加目标数"], 0
		return None
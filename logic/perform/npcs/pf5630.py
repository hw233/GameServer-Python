# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5630
	name = "独门手法"
	configInfo = {
		"概率":30,
	}
#导表结束

	def onSetup(self, w):
		self.setApply(w, "PF1232Ratio", self.configInfo["概率"])
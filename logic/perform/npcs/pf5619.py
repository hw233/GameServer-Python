# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5619
	name = "隐形剑诀"
	configInfo = {
		"治疗结果加成":10,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onCalCure", self.onCalCure)
		
	def onCalCure(self, att, vic, dam):
		count = 0
		warObj = att.war
		for w in warObj.idxList.itervalues():
			if w.hasApply("隐身"):
				count += 1
		return 0, count * self.configInfo["治疗结果加成"]
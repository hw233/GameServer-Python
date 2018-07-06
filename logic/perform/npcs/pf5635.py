# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5635
	name = "幻波仙池"
	applyList = {
		"破隐":True,
	}
	configInfo = {
		"伤害加成":40,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onTargetReceiveDamage", self.onTargetReceiveDamage)
		
	def onTargetReceiveDamage(self, att, vic, dp, attackType):
		if vic.hasApply("隐身"):
			return 0, self.configInfo["伤害加成"]
		return None
		
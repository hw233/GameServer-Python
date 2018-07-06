# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5129
	name = "逆境"
	configInfo = {
		"伤害加成":3,
		"次数限制":3,
	}
#导表结束
#当回合每受到一次伤害，则本回合造成的伤害增加3%，效果最多累积3次

	def onSetup(self, w):
		self.times = 0
		self.addFunc(w, "onAttacked", self.onAttacked)
		
	def onAttacked(self, att, vic, vicCast, dp, attackType):
		if vic.hasApply("PF5129Times") >= self.configInfo["次数限制"]:
			return
		vic.addBoutApply("PF5129Times", 1)
		vic.addBoutApply("物理伤害结果加成", self.configInfo["伤害加成"])
		vic.addBoutApply("法术伤害结果加成", self.configInfo["伤害加成"])

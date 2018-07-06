# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5137
	name = "大义"
	applyList = {
		"禁止逃跑":True,
	}
	configInfo = {
		"概率":6,
	}
#导表结束
#不会逃跑，不受恐惧、眩晕效果影响，并且受到物理伤害时有6%的几率将伤害变为1点

	def onSetup(self, w):
		self.addFunc(w, "onAbsorb", self.onAbsorb)
		self.setApply(w, self.name, True)
		
	def onAbsorb(self, att, vic, dp, attackType):
		if attackType.attackType not in phyAttackTypeList:
			return dp
		if rand(100) >= self.configInfo["概率"]:
			return dp
		return 1


from common import *		
from war.defines import *	
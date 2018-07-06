# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5125
	name = "坚韧"
	applyList = {
		"免疫暴击":True,
	}
	configInfo = {
		"概率":6,
	}
#导表结束
#不会受到暴击伤害，并且受到法术伤害时有6%的几率将伤害变为1点

	def onSetup(self, w):
		self.addFunc(w, "onAbsorb", self.onAbsorb)
		
	def onAbsorb(self, att, vic, dp, attackType):
		if attackType.attackType != ATTACK_TYPE_PERFORM_MAG:
			return dp
		if rand(100) >= self.configInfo["概率"]:
			return dp
		return 1


from common import *		
from war.defines import *	
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5318
	name = "百花庇护"
	applyList = {
		"免疫暴击":True,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if attackType.attackType != ATTACK_TYPE_PERFORM_MAG:
			return

		hp = dp * 7 / 100
		if hp:
			att.addHP(hp, att)
			
from war.defines import *
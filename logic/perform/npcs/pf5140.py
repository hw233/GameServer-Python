# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5140
	name = "益气"
	configInfo = {
		"真气":15,
	}
#导表结束
#造成法术伤害时，将目标受伤量的15%转化为主人的真气，群攻技能只对主目标有效

	def onSetup(self, w):
		if not w.isPet():
			return
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if dp <= 0:
			return
		if attackType.attackType != ATTACK_TYPE_PERFORM_MAG:
			return
		if vic.attackedIdx != 0:
			return
		
		mp = dp * self.configInfo["真气"] / 100
		roleW = att.war.getWarrior(att.ownerIdx)
		if roleW and not roleW.isDead():
			roleW.addMP(mp)

from common import *
from war.defines import *
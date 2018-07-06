# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5139
	name = "回生"
	configInfo = {
		"生命":15,
	}
#导表结束
#使用物理攻击时，将目标受伤量的15%转化为主人的生命，群攻技能只对主目标有效

	def onSetup(self, w):
		if not w.isPet():
			return
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if dp <= 0:
			return
		if attackType.attackType not in phyAttackTypeList:
			return
		if vic.attackedIdx != 0:
			return
		
		hp = dp * self.configInfo["生命"] / 100
		roleW = att.war.getWarrior(att.ownerIdx)
		if roleW and not roleW.isDead():
			roleW.addHP(hp)

from common import *
from war.defines import *
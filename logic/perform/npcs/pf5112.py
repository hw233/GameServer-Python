# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5112
	name = "叠刃"
	configInfo = {
		"概率":30,
		"伤害":40,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if vic.attackedIdx != 0: # 不是主目标
			return None
		if att.isDead() or vic.isDead():
			return
		if attackType.attackType not in phyAttackTypeList:
			return
		if attackType.isBack:
			return
		if rand(100) < self.configInfo["概率"]:
			hp = int(dp * self.configInfo["伤害"] / 100)
			vic.addHP(-hp, att)
			self.performSay(att)


from common import *
from war.defines import *

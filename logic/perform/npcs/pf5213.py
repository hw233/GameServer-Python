# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5213
	name = "高级连珠"
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if vic.attackedIdx != 0: # 不是主目标
			return None
		if att.isDead() or vic.isDead():
			return
		if attackType.attackType != ATTACK_TYPE_PERFORM_MAG:
			return
		if rand(100) < 30:
			hp = int(dp * 0.5)
			vic.addHP(-hp, att)
			self.performSay(att)


from common import *
from war.defines import *

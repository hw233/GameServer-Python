# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5116
	name = "杀戮"
	configInfo = {
		"伤害":70,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		self.addFunc(w, "onTargetReceiveDamage", self.onTargetReceiveDamage)

	def onAttack(self, att, vic, vicCast, dp, attackType):
		if attackType.attackType != ATTACK_TYPE_PHY:
			return
		if not vic.isDead():
			return
		if attackType.isBack:
			return
		
		vicNext = att.getEnemyTarget()
		if not vicNext:
			return

		self.ratio = 100 - self.configInfo["伤害"]
		att.targetIdx = vicNext.idx
		war.commands.doPhyAttack(att, True)
		
	def onTargetReceiveDamage(self, att, vic, dp, attackType):
		if not hasattr(self, "ratio"):
			return None
		ratio = self.ratio
		del self.ratio
		return 0, -ratio
		
from common import *
from war.defines import *
import war.commands
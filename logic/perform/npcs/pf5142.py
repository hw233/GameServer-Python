# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5142
	name = "乘胜"
	configInfo = {
		"伤害率":70,
	}
#导表结束
#使用普通攻击造成暴击时，将继续攻击下一个目标，造成70%的物理伤害

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		self.addFunc(w, "onTargetReceiveDamage", self.onTargetReceiveDamage)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if attackType.attackType != ATTACK_TYPE_PHY:
			return
		if not attackType.isCrit: # 没有暴击
			return
		if attackType.isBack: # 反击不算
			return
		
		for w in att.getEnemyList():
			if w is vic:
				continue
			self.ratio = 100 - self.configInfo["伤害率"]
			att.targetIdx = w.idx
			war.commands.doPhyAttack(att, True)
			break
			
	def onTargetReceiveDamage(self, att, vic, dp, attackType):
		if not hasattr(self, "ratio"):
			return None
		ratio = self.ratio
		del self.ratio
		return 0, -ratio
	
	
from common import *
from war.defines import *
import war.commands
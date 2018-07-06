# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5120
	name = "刺甲"
	configInfo = {
		"反弹概率":50,
		"伤害率":20,
	}
#导表结束
#免疫本场战斗第一次受到的伤害，如果该次伤害是物理伤害，则有50%的几率反弹20%的伤害给攻击者

	def onSetup(self, w):
		self.addFunc(w, "onAbsorb", self.onAbsorb)
		self.addFunc(w, "onAttacked", self.onAttacked)
		
	def onAttacked(self, att, vic, vicCast, dp, attackType):
		self.removeFunc(vic, "onAttacked") # 只会被调用一次
		if attackType.attackType not in phyAttackTypeList:
			return
		if att.hasApply("免疫反弹"):
			return
		if rand(100) >= self.configInfo["反弹概率"]:
			return
		hp = dp * self.configInfo["伤害率"] / 100
		att.addHP(-hp, vic)
	
	def onAbsorb(self, att, vic, dp, attackType):
		self.removeFunc(vic, "onAbsorb") # 只会被调用一次
		return 0
	
from common import *
from war.defines import *
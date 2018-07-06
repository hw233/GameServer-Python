# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5115
	name = "镜反"
	configInfo = {
		"概率":30,
		"伤害":25,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onReceiveDamage", self.onReceiveDamage)
		self.addFunc(w, "onAttacked", self.onAttacked)
		
	def onReceiveDamage(self, att, vic, dp, attackType):
		if attackType.attackType not in (ATTACK_TYPE_PHY, ATTACK_TYPE_PERFORM_PHY):
			return None
		if att.isDead():
			return None
		if att.hasApply("免疫反弹"):
			return None
		if rand(100) >= self.configInfo["概率"]:
			return None
		
		ratio = self.configInfo["伤害"]
		self.hp = dp * ratio / 100
		return 0, -ratio
		
	def onAttacked(self, att, vic, vicCast, dp, attackType):
		if not hasattr(self, "hp"):
			return
		if att.isDead():
			return
		hp = self.hp
		del self.hp
		att.addHP(-hp, vic)


from common import *
from war.defines import *
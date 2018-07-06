# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "反伤"
	type = BUFF_TYPE_BUFF
#导表结束
	ratio = 50 # 反弹比例
	hpLimit = 100 # 反弹上限

	def onSetup(self, w):
		self.addFunc(w, "onReceiveDamage", self.onReceiveDamage)
		self.addFunc(w, "onAttacked", self.onAttacked)
	
	def onReceiveDamage(self, att, vic, dp, attackType):
		if att.isDead():
			return 0, 0

		hp = int(dp * self.ratio / 100)
		hp = min(hp, self.hpLimit)
		if hp <= 0:
			return 0, 0

		self.hp = hp
		return 0, -self.ratio
	
	def onAttacked(self, att, vic, vicCast, dp, attackType):
		if not hasattr(self, "hp"):
			return
		buff.remove(vic, self.id)
		hp = self.hp
		del self.hp
		att.addHP(-hp, vic)
	
	def config(self, ratio, hpLimit):
		self.ratio = ratio
		self.hpLimit = hpLimit


import buff

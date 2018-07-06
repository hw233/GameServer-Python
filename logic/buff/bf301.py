# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "中毒"
	type = BUFF_TYPE_DEBUFF
#导表结束
	
	hpRatio = 3
	hpLimit = 100

	def onCleanRound(self, w):
		if w.isDead():
			return
		hp = min(self.hpLimit, w.getHPMax() * self.hpRatio / 100)
		w.addHP(-hp, w)

	def config(self, hpRatio, hpLimit):
		self.hpRatio = hpRatio
		self.hpLimit = hpLimit
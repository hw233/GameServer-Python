# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "祸水绵延"
	type = BUFF_TYPE_DEBUFF
#导表结束
	hpFirst = 20
	hp = 10

	def config(self, hpFirst, hp):
		self.hpFirst = hpFirst
		self.hp = hp
		if hasattr(self, "hasFirst"):
			del self.hasFirst
		
	def onCleanRound(self, w):
		if w.isDead():
			return
		if hasattr(self, "hasFirst"):
			w.addHP(-self.hp)
		else:
			w.addHP(-self.hpFirst)
			self.hasFirst = True
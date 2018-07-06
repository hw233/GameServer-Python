   # -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "阴阳"
	type = BUFF_TYPE_DEBUFF
#导表结束
	ratio = 10

	def onSetup(self, w):
		self.addFunc(w, "onReceiveDamage", self.onReceiveDamage)
		
	def onReceiveDamage(self, att, vic, dp, attackType):
		if att.gender == vic.gender:
			return 0, self.ratio
		return 0, 0
	
	def config(self, ratio):
		self.ratio = ratio

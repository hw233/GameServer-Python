# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5302
	name = "龟甲秘术"
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onReceiveDamage", self.onReceiveDamage)
		
	def onReceiveDamage(self, att, vic, dp, attackType):
		if vic.hp < vic.hpMax * 0.3:
			return 0, -25
		return None
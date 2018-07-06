# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "远树寒烟"
	type = BUFF_TYPE_DEBUFF
#导表结束

	ratio = 100
	
	def onSetup(self, w):
		self.addFunc(w, "onConsume", self.onConsume)
		
	def onConsume(self, att, vic, consumeName, consumeVal, attackType):
		if rand(100) < self.ratio:
			return consumeVal * 2
		return consumeVal
	
	
from common import *

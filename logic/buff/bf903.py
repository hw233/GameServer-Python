# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "魅惑"
	type = BUFF_TYPE_DEBUFF
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "invertDamage", self.invertDamage)
		self.addFunc(w, "invertCure", self.invertCure)

	def invertDamage(self, att, vic, dp, attackType):
		return dp
	
	def invertCure(self, att, vic, dp, attackType):
		return dp


from common import *
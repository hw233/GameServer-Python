# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "忠诚之心"
	type = BUFF_TYPE_BUFF
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAbsorb", self.onAbsorb)
		
	def onAbsorb(self, att, vic, dp, attackType):
		buff.remove(vic, self.id)
		return 0


import buff
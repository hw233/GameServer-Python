# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "金刚不坏"
	type = BUFF_TYPE_BUFF
#导表结束
	hp = 1

	def onSetup(self, w):
		self.addFunc(w, "onAbsorb", self.onAbsorb)
		
	def onAbsorb(self, att, vic, dp, attackType):
		if self.hp > dp:
			self.hp = self.hp - dp
			return 0
		else:
			buff.remove(vic, self.id)
			return dp - self.hp
		
		
from common import *
import buff
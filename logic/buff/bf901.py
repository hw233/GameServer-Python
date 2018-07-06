# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "无敌"
	type = BUFF_TYPE_BUFF
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAddBuff", self.onAddBuff)
		self.addFunc(w, "onAbsorb", self.onAbsorb)
		
	def onAddBuff(self, vic, bfObj, bout, att):
		if bfObj.type == BUFF_TYPE_SEAL: # 抗封
			buff.remove(vic, self.id)
			return 0
		return bout
	
	def onAbsorb(self, att, vic, dp, attackType):
		buff.remove(vic, self.id)
		return 0 # 完全吸收
		
	
import buff

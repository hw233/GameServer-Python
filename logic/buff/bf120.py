# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "龙象般若"
	type = BUFF_TYPE_BUFF
#导表结束

	def onCleanRound(self, w):
		if not hasattr(self, "mp"):
			return
		if w.isDead():
			return
		w.addMP(self.mp, w)
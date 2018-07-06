# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "立地生肌"
	type = BUFF_TYPE_BUFF
#导表结束
	hp = 1

	def onCleanRound(self, w):
		if w.isDead():
			return
		w.addHP(self.hp, w)
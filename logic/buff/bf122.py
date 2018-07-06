# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "五雷轰顶"
	type = BUFF_TYPE_DEBUFF
#导表结束
	hp = 1

	def onCleanRound(self, w):
		w.addHP(-self.hp)
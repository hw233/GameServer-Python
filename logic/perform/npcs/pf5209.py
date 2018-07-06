# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5209
	name = "高级无定"
#导表结束

	def onSetup(self, w):
		self.setApply(w, "额外物理伤害结果波动", (90, 125))
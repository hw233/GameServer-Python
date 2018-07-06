# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5110
	name = "无界"
#导表结束

	def onSetup(self, w):
		self.setApply(w, "额外法术伤害结果波动", (80, 120))
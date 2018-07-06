# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5111
	name = "封盾"
#导表结束

	def onSetup(self, w):
		self.addApply(w, "抵抗封印", 10)
		self.addApply(w, "法术伤害结果加成", -10)
		self.addApply(w, "物理伤害结果加成", -10)
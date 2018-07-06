# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5606
	name = "酒剑双绝"
#导表结束

	def onSetup(self, w):
		self.addApply(w, "物理暴击", 10)
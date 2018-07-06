# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3602
	name = "移形"
#导表结束

	def onSetup(self, w):
		w.addApply("物理躲闪率", 2)
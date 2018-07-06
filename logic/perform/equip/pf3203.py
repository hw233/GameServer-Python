# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3203
	name = "妙手"
#导表结束

	def onSetup(self, w):
		w.addApply("受到药品加成", 10)
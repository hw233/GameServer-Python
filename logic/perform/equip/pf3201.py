# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3201
	name = "灵药"
#导表结束

	def onSetup(self, w):
		w.addApply("使用药品加成", 10)
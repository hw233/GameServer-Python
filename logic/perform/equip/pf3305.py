# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3305
	name = "暗香"
#导表结束

	def onSetup(self, w):
		w.addApply("治疗结果加成", 2)
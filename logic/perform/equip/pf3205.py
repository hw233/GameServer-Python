# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3205
	name = "惠赠"
#导表结束

	def onSetup(self, w):
		w.addApply("药神", 1)
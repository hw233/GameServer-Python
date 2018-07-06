# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3601
	name = "形影"
#导表结束

	def onSetup(self, w):
		w.addApply("法术躲闪率", 2)
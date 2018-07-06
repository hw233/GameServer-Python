# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5501
	name = "死不瞑目"
#导表结束

	def onSetup(self, w):
		self.setApply(w, "不出场", True)
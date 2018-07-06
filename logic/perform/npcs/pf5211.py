# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5211
	name = "高级封盾"
#导表结束

	def onSetup(self, w):
		self.addApply(w, "抵抗封印", 10)
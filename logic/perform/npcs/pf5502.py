# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5502
	name = "免疫封印"
	buffId = 501
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAddWarrior", self.onAddWarrior)
		
	def onAddWarrior(self, w):
		buff.addOrReplace(w, self.buffId, 99)
		
		
import buff
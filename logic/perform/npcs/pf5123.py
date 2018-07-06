# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5123
	name = "迅捷"
	bout = 3
	buffId = 221
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAddWarrior", self.onAddWarrior)
	
	def onAddWarrior(self, w):
		bout = self.calBout(w, w, self.buffId)
		buff.addOrReplace(w, self.buffId, bout)


import buff
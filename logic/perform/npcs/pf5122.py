# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5122
	name = "披靡"
	bout = 3
	buffId = 220
#导表结束
#出战前3回合伤害结果提高15%

	def onSetup(self, w):
		self.addFunc(w, "onAddWarrior", self.onAddWarrior)
	
	def onAddWarrior(self, w):
		bout = self.calBout(w, w, self.buffId)
		buff.addOrReplace(w, self.buffId, bout)


import buff
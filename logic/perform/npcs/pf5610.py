# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5610
	name = "艳尸娘子"
#导表结束
#死亡时也会获得每回合的符能

	def onSetup(self, w):
		self.setApply(w, "回合末回复符能", True)
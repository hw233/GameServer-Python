# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3501
	name = "提携"
	bout = 8
	buffId = 219
#导表结束
#首只出战的异兽，对敌伤害结果+5%，持续8回合

	def onSetup(self, w):
		if not w.isRole():
			return
		self.roleId = w.getPID()
		w.war.addFunc("onAddWarrior", self.onAddWarrior)
		
	def onAddWarrior(self, w):
		if hasattr(self, "hasDone"):
			return
		if not w.isPet():
			return
		if w.ownerId != self.roleId:
			return
		
		roleW = w.war.getWarrior(w.ownerIdx)
		bout = self.calBout(roleW, w, self.buffId)
		buff.addOrReplace(w, self.buffId, bout, roleW)
		self.hasDone = True

import buff	
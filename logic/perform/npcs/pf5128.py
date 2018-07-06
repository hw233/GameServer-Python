# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5128
	name = "隐匿"
	bout = 3
	buffId = 223
#导表结束
#进入战斗隐形3回合，对敌人所有伤害减少20%，无法使用法术

	def onSetup(self, w):
		self.addFunc(w, "onAddWarrior", self.onAddWarrior)
	
	def onAddWarrior(self, w):
		bout = self.calBout(w, w, self.buffId)
		buff.addOrReplace(w, self.buffId, bout)


import buff
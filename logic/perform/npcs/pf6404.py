# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6404
	name = "降治疗"
	bout = 2
	buffId = 514
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if attackType.attackType not in phyAttackTypeList:
			return
		if dp <= 0:
			return
		if vic.isDead():
			return
		bout = self.calBout(att, vic, self.buffId)
		buff.addOrReplace(vic, self.buffId, bout, att)


from war.defines import *
import buff
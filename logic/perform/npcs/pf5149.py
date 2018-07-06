# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5149
	name = "壬水"
	configInfo = {
		"概率":20,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAbsorb", self.onAbsorb)

	def onAbsorb(self, att, vic, dp, attackType):
		if att.fiveElAttack != FIVE_EL_WATER:
			return dp
		if rand(100) >= self.configInfo["概率"]:
			return dp
		vic.addHP(dp)
		return 0
			
			
from common import *
from perform.defines import *
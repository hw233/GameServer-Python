# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5633
	name = "天魔噬焰"
	configInfo = {
		"封印命中":lambda HPR:20-HPR/5,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onCalSealHit", self.onCalSealHit)
		
	def onCalSealHit(self, att, vic, hitRatio, attackType):
		add = self.transCode(self.configInfo["封印命中"], att, vic)
		return add, 0

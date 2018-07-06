# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5307
	name = "怒打乾坤"
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onCalMagCritRatio", self.onCalCritRatio)
		self.addFunc(w, "onCalPhyCritRatio", self.onCalCritRatio)
		
	def onCalCritRatio(self, att, vic, attackType):
		hpLimit = att.hpMax * 50 / 100
		if att.hp >= hpLimit:
			return None
		
		hpStep = int(att.hpMax * 0.05)
		add = (hpLimit - att.hp) / hpStep * 3
		return 10 + add, 0
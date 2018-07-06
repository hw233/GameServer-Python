# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3102
	name = "持身"
	configInfo = {
		"真气":50,
	}
#导表结束	

	def onSetup(self, w):
		self.addFunc(w, "onDefend", self.onDefend)
		
	def onDefend(self, att, vic, attackType):
		vic.addMP(self.configInfo["真气"])
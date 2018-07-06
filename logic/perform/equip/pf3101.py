# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 3101
	name = "盈袖"
	configInfo = {
		"概率":15,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onConsume", self.onConsume)
		
	def onConsume(self, att, vic, consumeName, consumeVal, attackType):
		if consumeName == "真气" and rand(100) < self.configInfo["概率"]:
			return 0
		return consumeVal
	
from common import *

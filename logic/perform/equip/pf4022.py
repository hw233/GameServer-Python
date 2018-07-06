# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4022
	name = "摧眉折腰"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	power = 100
	consumeList = {
		"愤怒": 40,
	}
	configInfo = {
		"符能":60,
	}
#导表结束

	def buff(self, att, vic, targetCount):
		CustomPerform.buff(self, att, vic, targetCount)
		fuWen = self.transCode(self.configInfo["符能"], att, vic)
		vic.addFuWen(-fuWen)

# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4019
	name = "青莲净心"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	consumeList = {
		"愤怒": 45,
	}
	configInfo = {
		"愤怒":55,
	}
#导表结束
#减少敌方单体目标55点怒气

	def buff(self, att, vic, targetCount):
		CustomPerform.buff(self, att, vic, targetCount)
		sp = self.configInfo["愤怒"]
		vic.addSP(-sp)

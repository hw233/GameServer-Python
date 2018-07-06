# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5719
	name = "阴阳"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 99
	bout = 2
	readyBout = 2
	frozenBout = 4
	buffId = 906
	configInfo = {
		"伤害":10,
	}
#导表结束

	def afterBuff(self, att, vic, bfObj, targetCount):
		if bfObj:
			bfObj.config(self.configInfo["伤害"])
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4013
	name = "万世不竭"
	targetType = PERFORM_TARGET_SELF
	targetCount = 1
	consumeList = {
		"愤怒": 90,
	}
	configInfo = {
		"真气":lambda mpMax:mpMax*15/100+250,
	}
#导表结束

	def buff(self, att, vic, targetCount):
		CustomPerform.buff(self, att, vic, targetCount)
		mp = self.transCode(self.configInfo["真气"], att, vic)
		att.addMP(mp, att)

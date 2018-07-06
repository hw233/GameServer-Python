# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4012
	name = "俯仰自得"
	targetType = PERFORM_TARGET_SELF
	targetCount = 1
	consumeList = {
		"愤怒": 60,
	}
	configInfo = {
		"真气":lambda mpMax:mpMax*10/100+150,
	}
#导表结束
#回复自己10%+150点真气

	def buff(self, att, vic, targetCount):
		CustomPerform.buff(self, att, vic, targetCount)
		mp = self.transCode(self.configInfo["真气"], att, vic)
		att.addMP(mp, att)
		

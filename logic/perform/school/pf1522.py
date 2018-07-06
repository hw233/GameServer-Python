# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import CurePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1522
	name = "通幽续命"
	targetType = PERFORM_TARGET_SELF
	targetCount = 1
	damage = lambda self,SLV:SLV*2+20
	power = 100
	consumeList = {
		"真气": lambda SLV:SLV*1+20,
		"符能": 20,
	}
	speRatio = 104
	configInfo = {
		"恢复真气":200,
	}
#导表结束

	def onCure(self, att, vic, vicCast, dp, targetCount):
		mp = self.transCode(self.consumeList["真气"], att, vic)
		if mp > 0:
			mp = int(mp * self.configInfo["恢复真气"] / 100)
			vic.addMP(mp)

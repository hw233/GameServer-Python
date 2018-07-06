# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import CurePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5713
	name = "气疗"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 3
	readyBout = 3
	frozenBout = 3
	configInfo = {
		"治疗":lambda phyDefV,VLV:(phyDefV-40)*200/((4.5*VLV)+1),
		"治疗上限":lambda VLV:VLV*10+10,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		dam = self.transCode(self.configInfo["治疗"], att, vic)
		damMax = self.transCode(self.configInfo["治疗上限"], att, vic)
		return min(dam, damMax)

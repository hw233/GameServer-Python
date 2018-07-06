# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5708
	name = "反伤"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	bout = 1
	readyBout = 2
	frozenBout = 4
	buffId = 902
	configInfo = {
		"反弹比例":50,
		"反弹上限":lambda VLV:VLV*30,
	}
#导表结束

	def afterBuff(self, att, vic, bfObj, targetCount):
		if bfObj:
			hpLimit = self.transCode(self.configInfo["反弹上限"], att, vic)
			bfObj.config(self.configInfo["反弹比例"], hpLimit)

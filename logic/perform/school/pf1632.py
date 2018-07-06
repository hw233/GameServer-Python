# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1632
	name = "龙象般若"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+3
	boutMax = 3
	consumeList = {
		"符能": 15,
	}
	buffId = 120
	speRatio = 100
#导表结束

	def afterBuff(self, att, vic, bfObj, targetCount):
		CustomPerform.afterBuff(self, att, vic, bfObj, targetCount)

		if not bfObj:
			return

		mp = self.transCode("SLV*1.5+30", att, vic)
		mpBuff = self.transCode("SLV*1.2+30", att, vic)
		vic.addMP(mp, att)
		bfObj.mp = mpBuff

# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1231
	name = "雪映晴"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 5
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+5
	boutMax = 5
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	buffId = 105
	speRatio = 100
#导表结束
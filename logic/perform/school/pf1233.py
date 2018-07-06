# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1233
	name = "雪满山"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = lambda self,SLV:SLV/35+3
	targetCountMax = 5
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+2
	boutMax = 2
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
		"符能": 40,
	}
	buffId = 107
	speRatio = 100
#导表结束
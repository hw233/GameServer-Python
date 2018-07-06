# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1431
	name = "百足蛊"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = lambda self,SLV:SLV/35+3
	targetCountMax = 5
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+5
	boutMax = 5
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 10,
	}
	buffId = 112
	speRatio = 100
#导表结束

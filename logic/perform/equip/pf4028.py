# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4028
	name = "秋水流光"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	bout = 99
	power = 100
	consumeList = {
		"愤怒": 40,
	}
	buffId = 207
#导表结束
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4027
	name = "长风破浪"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	bout = 99
	power = 100
	consumeList = {
		"愤怒": 80,
	}
	buffId = 206
#导表结束
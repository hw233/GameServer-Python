# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4025
	name = "吴钩霜雪"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	bout = 99
	power = 100
	consumeList = {
		"愤怒": 70,
	}
	buffId = 204
#导表结束
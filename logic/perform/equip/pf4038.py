# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4038
	name = "天寒日暮"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = 99
	power = 100
	consumeList = {
		"愤怒": 35,
	}
	buffId = 217
#导表结束
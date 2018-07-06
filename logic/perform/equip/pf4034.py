# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4034
	name = "落木萧萧"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = 99
	power = 100
	consumeList = {
		"愤怒": 35,
	}
	buffId = 213
#导表结束
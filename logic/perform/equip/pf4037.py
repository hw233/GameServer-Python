# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4037
	name = "四座无言"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 99
	bout = 99
	power = 100
	consumeList = {
		"愤怒": 100,
	}
	buffId = 216
#导表结束
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4032
	name = "放下屠刀"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = 99
	power = 100
	consumeList = {
		"愤怒": 30,
	}
	buffId = 211
#导表结束
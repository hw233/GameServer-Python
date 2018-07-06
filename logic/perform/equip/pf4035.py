# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4035
	name = "铁衣难着"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 99
	bout = 99
	power = 100
	consumeList = {
		"愤怒": 80,
	}
	buffId = 214
#导表结束
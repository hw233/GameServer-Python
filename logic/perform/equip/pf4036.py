# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4036
	name = "沾衣欲湿"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = 99
	power = 100
	consumeList = {
		"愤怒": 30,
	}
	buffId = 215
#导表结束
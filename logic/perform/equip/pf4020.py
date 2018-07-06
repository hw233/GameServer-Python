# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4020
	name = "霜凄万木"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 4
	bout = 3
	power = 100
	consumeList = {
		"愤怒": 100,
	}
	buffId = 201
#导表结束
#作用敌方4个目标，使目标3回合内接受任何治疗的效果降低50%
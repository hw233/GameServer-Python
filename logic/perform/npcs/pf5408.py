# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5408
	name = "地裂天崩"
	fiveEl = FIVE_EL_EARTH
	targetType = PERFORM_TARGET_ENEMY
	targetCount = lambda self,LV:LV/60+2
	damage = lambda self,LV:LV*2+20
	power = 100
	consumeList = {
		"真气": 50,
	}
#导表结束
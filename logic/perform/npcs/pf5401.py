# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5401
	name = "玄冰咒"
	fiveEl = FIVE_EL_WATER
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	damage = lambda self,LV:LV*2+20
	power = 100
	consumeList = {
		"真气": 30,
	}
#导表结束

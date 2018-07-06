# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1691
	name = "金刚伏魔"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 5
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"愤怒": 120,
	}
	speRatio = 100
#导表结束
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1511
	name = "血魔焰"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1+20,
	}
	recoverList = {
		"符能": 20,
	}
	speRatio = 100
#导表结束
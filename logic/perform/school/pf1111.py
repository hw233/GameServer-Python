# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1111
	name = "御剑术"
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

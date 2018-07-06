# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1212
	name = "风神枪"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = lambda self,SLV:SLV/35+3
	targetCountMax = 5
	damage = lambda self,SLV:SLV*2+20
	power = 60
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 5,
	}
	speRatio = 100
#导表结束
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1531
	name = "血雨腥风"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = lambda self,SLV:SLV/25+3
	targetCountMax = 6
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 10,
	}
	speRatio = 106
#导表结束
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import RemotePhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1112
	name = "百剑绕指"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = lambda self,SLV:SLV/35+3
	targetCountMax = 5
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 5,
	}
	speRatio = 100
#导表结束
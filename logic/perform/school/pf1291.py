# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1291
	name = "月下独酌"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 5
	damage = lambda self,SLV:SLV*2+20
	power = 60
	consumeList = {
		"愤怒": 120,
	}
	recoverList = {
		"符能": 5,
	}
	speRatio = 100
#导表结束
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import RemotePhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1132
	name = "混元一气诀"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 5
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1+30,
		"符能": 30,
	}
	speRatio = 100
#导表结束

	def checkTarget(self, att, vic, vicCast):
		for posList in line2PosList.values():
			if vic.pos in posList and vicCast.pos in posList:
				return 1
		return 0
	
line2PosList = {
	1: (1, 2, 3, 4, 5,),
	2: (6, 7, 8, 9, 10,),
	3: (11, 12, 13,),
	4: (14,),
}
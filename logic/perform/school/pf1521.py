# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1521
	name = "九幽阴风"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = lambda self,SLV:SLV/30+2
	targetCountMax = 4
	bout = lambda self,LV,SLV:(SLV-LV+2)/10+5
	boutMax = 5
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 10,
	}
	buffId = 115
	speRatio = 103
#导表结束

	def keyForSortTarget(self, w):
		if buff.has(w, self.buffId):
			hasBuff = 1
		else:
			hasBuff = 0
			
		return hasBuff, -w.getMagDamAll()
	

import buff
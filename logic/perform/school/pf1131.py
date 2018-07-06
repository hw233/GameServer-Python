# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1131
	name = "纯阳无极诀"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 5
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+5
	boutMax = 5
	consumeList = {
		"真气": lambda SLV:SLV*1+20,
	}
	recoverList = {
		"符能": 10,
	}
	buffId = 101
	speRatio = 100
#导表结束

	def keyForSortTarget(self, w):
		if buff.has(w, self.buffId):
			hasBuff = 1
		else:
			hasBuff = 0
		return hasBuff, -w.getPhyDamAll()


import buff
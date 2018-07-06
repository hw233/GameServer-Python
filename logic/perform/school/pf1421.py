# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import SealPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1421
	name = "迷魂咒"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+4
	boutMax = 4
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 10,
	}
	buffId = 109
	speRatio = 100
	hitRatio = lambda self,SLV,VLV:(SLV-VLV)*2+70
#导表结束

	def calTargetCount(self, att):
		'''计算目标数
		'''
		targetCount = CustomPerform.calTargetCount(self, att)
		for func in att.getFuncList("onCalTargetCount1421"):
			targetCount = func(att, targetCount)
		return targetCount
		
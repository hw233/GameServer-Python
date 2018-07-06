# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import CurePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4006
	name = "绿蚁红泥"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	consumeList = {
		"愤怒": 135,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		if att == vic: #不包括自己
			return 0
		dp = min(vic.hpMax * 25 / 100, vic.level * 12)
		return dp
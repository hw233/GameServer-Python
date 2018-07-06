# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import CurePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4003
	name = "清风入松"
	targetType = PERFORM_TARGET_SELF
	targetCount = 1
	consumeList = {
		"愤怒": 60,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dp = min(vic.hpMax * 25 / 100, vic.level * 12)
		return dp
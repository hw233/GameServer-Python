# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import CurePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4004
	name = "一蓑风雨"
	targetType = PERFORM_TARGET_SELF
	targetCount = 1
	consumeList = {
		"愤怒": 130,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dp = min(vic.hpMax * 50 / 100, vic.level * 20)
		return dp
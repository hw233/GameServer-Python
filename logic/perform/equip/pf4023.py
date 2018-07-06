# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4023
	name = "远树寒烟"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = 3
	power = 100
	consumeList = {
		"愤怒": 60,
	}
	buffId = 202
	configInfo = {
		"概率":70,
	}
#导表结束
#敌方单体目标3回合内使用技能有70%的几率消耗翻倍

	def afterBuff(self, att, vic, bfObj, targetCount):
		if bfObj:
			bfObj.ratio = self.configInfo["概率"]

		

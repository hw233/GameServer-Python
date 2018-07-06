# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import PhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4021
	name = "挥刃弯弓"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	power = 100
	consumeList = {
		"愤怒": 80,
	}
	configInfo = {
		"伤害系数":1.2,
		"真气":lambda mpV:mpV*20/100,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dam = CustomPerform.calDamage(self, att, vic, damRatio)
		return int(dam * self.configInfo["伤害系数"])
	
	def afterAttack(self, att, vic, vicCast, dp, targetCount):
		CustomPerform.afterAttack(self, att, vic, vicCast, dp, targetCount)
		
		if dp > 0:
			mp = self.transCode(self.configInfo["真气"], att, vic)
			vic.addMP(-mp, att)

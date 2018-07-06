# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5705
	name = "破魔"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 3
	readyBout = 2
	frozenBout = 3
	configInfo = {
		"伤害":lambda VLV,magDefV:(magDefV-40)*200/((4.5*VLV)+1),
		"伤害上限":lambda VLV:VLV*10+10,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dam = self.transCode(self.configInfo["伤害"], att, vic)
		damMax = self.transCode(self.configInfo["伤害上限"], att, vic)
		return min(dam, damMax)

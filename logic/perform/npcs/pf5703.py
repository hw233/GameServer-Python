# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5703
	name = "破术"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 3
	readyBout = 2
	frozenBout = 3
	configInfo = {
		"伤害":lambda magDamV,VLV:(magDamV-60)*200/((7.5*VLV)+1),
		"伤害上限":lambda VLV:VLV*10+10,
	}
#导表结束

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dam = self.transCode(self.configInfo["伤害"], att, vic)
		damMax = self.transCode(self.configInfo["伤害上限"], att, vic)
		return min(dam, damMax)

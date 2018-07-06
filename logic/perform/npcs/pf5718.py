# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5718
	name = "混沌"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 3
	readyBout = 2
	frozenBout = 3
	configInfo = {
		"玩家伤害":-50,
		"非玩家伤害":50,
		"伤害":lambda hpBaseV:hpBaseV*0.1,
	}
#导表结束

	def calDamageRatio(self, att, vic, vicCast, targetCount):
		damRatio = CustomPerform.calDamageRatio(self, att, vic, vicCast, targetCount)
		if vic.isRole():
			ratio = self.configInfo["玩家伤害"]
		else:
			ratio = self.configInfo["非玩家伤害"]
		damRatio = int(damRatio * (100 + ratio) / 100)
		return damRatio
	
	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		dam = self.transCode(self.configInfo["伤害"], att, vic)
		return dam * damRatio / 100
	
	def getValueByVarName(self, varName, att=None, vic=None):
		if varName == "hpBaseV":
			info = monsterBase.getBaseAbleInfo(vic.level)
			return info["生命"]
		return CustomPerform.getValueByVarName(self, varName, att, vic)
	
import monsterBase

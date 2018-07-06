# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1211
	name = "风雷弹"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	damage = lambda self,SLV:SLV*2+20
	power = 60
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 10,
	}
	speRatio = 100
	configInfo = {
		"治疗":lambda SLV:SLV*2+20,
		"治疗威力":50,
		"目标数":5,
	}
#导表结束

	def perform(self, att, vicCast):
		CustomPerform.perform(self, att, vicCast)
		
		targetList = self.getPerformTargetList(att, att, 99)
		targetList.sort(key=lambda w:w.hp)
		targetCount = self.configInfo["目标数"]
		targetList = targetList[:targetCount]
		targetCount = len(targetList)
		damRatio = self.calDamageRatio(att, vicCast, vicCast, targetCount)
		for vic in targetList:
			if vic.isDead():
				continue
			dp = self.calCure(att, vic, vicCast, damRatio)
			vic.addHP(dp, att)
				
	def calCure(self, att, vic, vicCast, damRatio):
		magDam = int(self.transCode(self.configInfo["治疗"], att, vic))
		power = self.configInfo["治疗威力"]
		dp = att.calCure(vic, magDam, power, damRatio, self.getAttackType())
		return dp
				
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1623
	name = "步步生莲"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+5
	boutMax = 5
	damage = lambda self,SLV:SLV*2+20
	power = 100
	consumeList = {
		"真气": lambda SLV:SLV*1.2+40,
		"符能": 30,
	}
	buffId = 118
	speRatio = 100
	configInfo = {
		"次数":5,
	}
#导表结束

	def afterBuff(self, att, vic, bfObj, targetCount):
		CustomPerform.afterBuff(self, att, vic, bfObj, targetCount)

		if not bfObj:
			return

		times = self.configInfo["次数"]
		if att.hasApply("弹跳次数"):
			times += att.hasApply("弹跳次数")
		bfObj.config(self, att, targetCount, times)
	
	def calCure(self, att, vic, vicCast, targetCount):
		damRatio = self.calDamageRatio(att, vic, vicCast, targetCount)
		magDam = self.getDamage(att, vic)
		dp = att.calCure(vic, magDam, self.power, damRatio, self.getAttackType())
		return dp
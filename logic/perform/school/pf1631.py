# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1631
	name = "金刚不坏"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = lambda self,LV:LV/50+2
	targetCountMax = 3
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+4
	boutMax = 4
	damage = lambda self,SLV:SLV*2+20
	power = 60
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 10,
	}
	buffId = 119
	speRatio = 120
#导表结束

	def afterBuff(self, att, vic, bfObj, targetCount):
		CustomPerform.afterBuff(self, att, vic, bfObj, targetCount)

		if not bfObj:
			return

		bfObj.hp = self.calCure(att, vic, vic, targetCount)

	def calCure(self, att, vic, vicCast, targetCount):
		damRatio = self.calDamageRatio(att, vic, vicCast, targetCount)
		magDam = self.getDamage(att, vic)
		dp = att.calCure(vic, magDam, self.power, damRatio, self.getAttackType())
		return dp
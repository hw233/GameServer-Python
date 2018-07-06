# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1633
	name = "洗髓易筋"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+3
	boutMax = 3
	damage = lambda self,SLV:SLV*2+20
	power = 120
	consumeList = {
		"真气": lambda SLV:SLV*1.2+40,
		"符能": 40,
	}
	buffId = 121
	speRatio = 150
#导表结束

	def afterBuff(self, att, vic, bfObj, targetCount):
		CustomPerform.afterBuff(self, att, vic, bfObj, targetCount)

		if not bfObj:
			return

		bfObj.hp = self.calCure(att, vic, vic, targetCount)
		if att.hasApply("PF5622Ratio"):
			bfObj.ratio = att.hasApply("PF5622Ratio")

	def calCure(self, att, vic, vicCast, targetCount):
		damRatio = self.calDamageRatio(att, vic, vicCast, targetCount)
		magDam = self.getDamage(att, vic)
		dp = att.calCure(vic, magDam, self.power, damRatio, self.getAttackType())
		return dp
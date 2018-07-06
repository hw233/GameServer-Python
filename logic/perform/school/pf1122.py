# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import RemotePhyAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1122
	name = "五雷符法"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = lambda self,LV:LV/35+3
	targetCountMax = 5
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+5
	boutMax = 5
	damage = lambda self,SLV:SLV*2+20
	power = 100
	consumeList = {
		"真气": lambda SLV:SLV*1.2+30,
		"符能": 30,
	}
	buffId = 122
	speRatio = 100
#导表结束

	def afterAttack(self, att, vic, vicCast, dp, targetCount):
		CustomPerform.afterAttack(self, att, vic, vicCast, dp, targetCount)
		if dp > 0 and vic.inWar():
			bout = self.calBout(att, vic, self.buffId)
			bfObj = buff.addOrReplace(vic, self.buffId, bout, att)
			if bfObj:
				bfObj.hp = dp * 10 / 100
			

import buff
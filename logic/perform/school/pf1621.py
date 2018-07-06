# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import CurePerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1621
	name = "立地生佛"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 2
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+5
	boutMax = 5
	damage = lambda self,SLV:SLV*2+20
	power = 80
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
	}
	recoverList = {
		"符能": 10,
	}
	buffId = 117
	speRatio = 100
#导表结束

	def onCure(self, att, vic, vicCast, dp, targetCount):
		'''治疗时
		'''
		bout = self.calBout(att, vic, self.buffId)
		bfObj = buff.addOrReplace(vic, self.buffId, bout, att)
		if bfObj:
			bfObj.hp = dp * 60 / 100

import buff
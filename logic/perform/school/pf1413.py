# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1413
	name = "逐蝎术"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 1
	bout = 1
	damage = lambda self,SLV:SLV*2+20
	power = 60
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
		"符能": 20,
	}
	buffId = 124
	speRatio = 100
#导表结束

	def afterPerform(self, att, vicCast):
		CustomPerform.afterPerform(self, att, vicCast)
		if att.isDead():
			return
		bout = self.calBout(att, att, self.buffId)
		buff.addOrReplace(att, self.buffId, bout, att)

import buff
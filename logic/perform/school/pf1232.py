# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import ReSealPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1232
	name = "雪飘尘"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 1
	bout = 2
	consumeList = {
		"真气": lambda SLV:SLV*1.2+20,
		"符能": 10,
	}
	buffId = 106
	speRatio = 100
#导表结束

	def afterBuff(self, att, vic, bfObj, targetCount):
		CustomPerform.afterBuff(self, att, vic, bfObj, targetCount)

		if not bfObj:
			return

		buffList = vic.buffList[BUFF_TYPEPOS_SEAL]
		for bfObj in buffList:
			if bfObj:
				buff.remove(vic, bfObj.id)
		
		bout = self.calBout(att, vic, self.buffId)
		buff.addOrReplace(vic, self.buffId, bout, att)
		
	def afterPerform(self, att, vicCast):
		CustomPerform.afterPerform(self, att, vicCast)
				
		ratio = att.hasApply("PF1232Ratio")
		if not ratio or rand(100) >= ratio:
			return
		if att.hasApply("PF1232Done"):
			return
		
		for w in att.getFriendList():
			if w.inSeal():
				att.setBoutApply("PF1232Done", True)
				self.perform(att, w)
				break
		

from common import *
from buff.defines import *
import buff
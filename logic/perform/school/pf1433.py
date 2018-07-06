# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 1433
	name = "隐身蛊"
	targetType = PERFORM_TARGET_SELF
	targetCount = 1
	bout = lambda self,SLV,VLV:(SLV-VLV+2)/10+5
	boutMax = 5
	consumeList = {
		"真气": lambda SLV:SLV*1.2+40,
		"符能": 40,
	}
	buffId = 114
	speRatio = 100
#导表结束

	def validPerform(self, att, needTips):
		'''检查施法
		'''
		if hasattr(self, "hasPerformed"):
			if needTips:
				message.tips(att.getPID(), "一场战斗只能使用一次")
			return False
		return CustomPerform.validPerform(self, att, needTips)
	
	def afterPerform(self, att, vicCast):
		CustomPerform.afterPerform(self, att, vicCast)
		self.hasPerformed = True
	
import message

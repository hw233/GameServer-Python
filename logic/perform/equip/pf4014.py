# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4014
	name = "碧山孤月"
	targetType = PERFORM_TARGET_ANY
	targetCount = 99
	consumeList = {
		"愤怒": 100,
	}
#导表结束

	def customPerformTargetList(self, att, vicCast, targetCount):
		warObj = att.war
		targetList = []
		for w in warObj.idxList.itervalues():
			if w.isDead():
				continue
			if not w.isVisible(att):
				continue
			targetList.append(w)
		return targetList

	def buff(self, att, vic, targetCount):
		CustomPerform.buff(self, att, vic, targetCount)
		removeList = []
		for buffList in vic.buffList.values():
			for buffObj in buffList:
				if buffObj:
					removeList.append(buffObj.id)
					
		for buffId in removeList:
			buff.remove(vic, buffId)
						
import buff
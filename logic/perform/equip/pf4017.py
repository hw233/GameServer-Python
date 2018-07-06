# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4017
	name = "松月夜凉"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	consumeList = {
		"愤怒": 125,
	}
#导表结束

	def buff(self, att, vic, targetCount):
		CustomPerform.buff(self, att, vic, targetCount)
		removeList = []
		for pos in (BUFF_TYPEPOS_DEBUFF, BUFF_TYPEPOS_SEAL):
			for buffObj in vic.buffList[pos]:
				if buffObj:
					removeList.append(buffObj.id)
		
		for buffId in removeList:
			buff.remove(vic, buffId)

from buff.defines import *
import buff
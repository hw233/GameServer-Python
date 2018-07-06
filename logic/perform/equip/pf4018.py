# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 4018
	name = "荷风竹露"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	consumeList = {
		"愤怒": 150,
	}
	configInfo = {
		"生命":lambda hpMaxV:hpMaxV*15/100,
		"上限":lambda VLV:VLV*12,
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
					
		hpLimit = self.transCode(self.configInfo["上限"], att, vic)
		hp = self.transCode(self.configInfo["生命"], att, vic)
		hp = min(hp, hpLimit)
		vic.addHP(hp, att)


from buff.defines import *
import buff
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5604
	name = "刚正不阿"
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onEndRound", self.onEndRound)
		
	def onEndRound(self, w):
		if rand(100) >= 20:
			return
		
		buffList = []
		for pos in (BUFF_TYPEPOS_DEBUFF, BUFF_TYPEPOS_SEAL):
			for buffObj in w.buffList[pos]:
				if buffObj:
					buffList.append(buffObj.id)
					
		if buffList:
			buffId = buffList[rand(len(buffList))]
			buff.remove(w, buffId)


from common import *
from buff.defines import *
import buff
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5632
	name = "七矮之首"
	configInfo = {
		"回合":3,
	}
#导表结束
#每3回合清除自身的异常状态

	def onSetup(self, w):
		self.addFunc(w, "onEndRound", self.onEndRound)
		
	def onEndRound(self, w):
		bout = self.configInfo["回合"] - 1
		if w.bout % bout != 0:
			return
		
		removeList = []
		for pos in (BUFF_TYPEPOS_DEBUFF, BUFF_TYPEPOS_SEAL):
			for buffObj in w.buffList[pos]:
				if buffObj:
					removeList.append(buffObj.id)
					
		for buffId in removeList:
			buff.remove(w, buffId)
		
from buff.defines import *
import buff		
		
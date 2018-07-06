# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5136
	name = "清心"
	configInfo = {
		"概率":lambda LV,con:7-(con-10)/(LV+1),
	}
#导表结束
#每回合有7%-(体质点数-10)/等级*1%的几率解除主人的封印状态

	def onSetup(self, w):
		if not w.isPet():
			return
		self.addFunc(w, "onEndRound", self.onEndRound)
		
	def onEndRound(self, w):
		ratio = self.transCode(self.configInfo["概率"], w)
		if rand(100) >= ratio:
			return
		
		roleW = w.war.getWarrior(w.ownerIdx)
		if not roleW:
			return
		
		removeList = []
		for buffObj in roleW.buffList[BUFF_TYPEPOS_SEAL]:
			if buffObj:
				removeList.append(buffObj.id)
		
		for buffId in removeList:
			buff.remove(roleW, buffId)
			
from common import *
from buff.defines import *
import buff
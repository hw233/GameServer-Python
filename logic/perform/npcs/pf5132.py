# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5132
	name = "破封"
	configInfo = {
		"概率":60,
	}
#导表结束
#异兽进入战场时，60%的几率解除主人的封印状态
	def onSetup(self, w):
		if not w.isPet():
			return
		self.addFunc(w, "onSummoned", self.onSummoned)
		
	def onSummoned(self, att, vic):
		if rand(100) >= self.configInfo["概率"]:
			return
		
		removeList = []
		for buffObj in att.buffList[BUFF_TYPEPOS_SEAL]:
			if buffObj:
				removeList.append(buffObj.id)
		
		for buffId in removeList:
			buff.remove(att, buffId)
			
from common import *
from buff.defines import *
import buff
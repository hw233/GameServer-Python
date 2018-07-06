# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "混乱"
	type = BUFF_TYPE_DEBUFF
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onCommand", self.onCommand)
		
	def onCommand(self, att):
		targetList =  []
		warObj = att.war
		for w in warObj.idxList.itervalues():
			if w is att:
				continue
			if not w.isVisible(att):
				continue
			targetList.append(w)
		
		import war.commands
		if targetList:
			w = targetList[rand(len(targetList))]
			war.commands.setCommand(warObj, att, CMD_TYPE_PHY, targetIdx=w.idx)
		else:
			war.commands.setCommand(warObj, att, CMD_TYPE_WAIT)


from common import *
from war.defines import *
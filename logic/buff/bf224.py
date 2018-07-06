# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "恐惧"
	type = BUFF_TYPE_SPECIAL
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onNewRound", self.onNewRound)
		
	def onNewRound(self, w):
		import war.commands
		war.commands.setCommand_Defend(w.war, w)

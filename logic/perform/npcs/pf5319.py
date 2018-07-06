# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5319
	name = "忠诚之心"
	bout = 99
	buffId = 405
#导表结束

	def onSetup(self, w):
		w.protectOwnerRatio = 50 # 自动保护主人概率
		self.addFunc(w, "beforeDie", self.beforeDie)
		
	def beforeDie(self, vic, att):
		if not vic.isPet():
			return
		roleW = vic.war.getWarrior(vic.ownerIdx)
		if not roleW:
			return
		
		bout = self.calBout(vic, roleW, self.buffId)
		buffObj = buff.addOrReplace(roleW, self.buffId, bout, vic)
		
		
			
import buff
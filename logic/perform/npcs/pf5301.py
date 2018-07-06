# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5301
	name = "灵草冥毒"
	bout = 2
	buffId = 401
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if vic != vicCast: # 不是主目标 
			return
		if dp <= 0:
			return
		if not vic.inWar():
			return
		if not (rand(100) < 20):
			return
		bout = self.calBout(att, vic, self.buffId)
		buffObj = buff.addOrReplace(vic, self.buffId, bout, att)
		if buffObj:
			hp = (att.level * 3 + 10)
			buffObj.config(hp)

from common import *
import buff
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5313
	name = "散魂蝎毒"
	bout = 2
	buffId = 406
	configInfo = {
		"概率":20,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if not vic.isDead():
			return
		if not vic.inWar():
			return
		if rand(100) >= self.configInfo["概率"]:
			return
		
		bout = self.calBout(att, vic, self.buffId)
		buff.addOrReplace(vic, self.buffId, bout, att)
		
		
from common import *
import buff
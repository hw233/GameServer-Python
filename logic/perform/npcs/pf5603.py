# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5603
	name = "守正僻邪"
	bout = 2
	buffId = 301
	configInfo = {
		"概率":60,
		"生命":3,
		"生命上限":lambda LV:LV*5,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if dp <= 0:
			return
		if vic.isDead():
			return
		if rand(100) >= self.configInfo["概率"]:
			return
				
		bout = self.calBout(att, vic, self.buffId)
		buffObj = buff.addOrReplace(vic, self.buffId, bout, att)
		if buffObj:
			hpRatio = self.configInfo["生命"]
			hpLimit = self.transCode(self.configInfo["生命上限"], att)
			buffObj.config(hpRatio, hpLimit)
		
		
from common import *
import buff
		
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5629
	name = "唐门暗器"
	bout = 2
	buffId = 301
	configInfo = {
		"概率":60,
		"生命":3,
		"生命上限":lambda LV:LV*5,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttacked", self.onAttacked)
		
	def onAttacked(self, att, vic, vicCast, dp, attackType):
		if att.isDead():
			return
		if rand(100) >= self.configInfo["概率"]:
			return
		
		bout = self.calBout(vic, att, self.buffId)
		buffObj = buff.addOrReplace(att, self.buffId, bout, vic)
		if buffObj:
			hpRatio = self.configInfo["生命"]
			hpLimit = self.transCode(self.configInfo["生命上限"], vic)
			buffObj.config(hpRatio, hpLimit)
			self.performSay(vic)

from common import *
import buff
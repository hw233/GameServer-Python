# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6405
	name = "碧目天罗"
	bout = 2
	buffId = 109
	configInfo = {
		"概率":10,
	}
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAttacked", self.onAttacked)
		
	def onAttacked(self, att, vic, vicCast, dp, attackType):
		if dp <= 0:
			return
		if att.isDead():
			return
		if rand(100) >= self.configInfo["概率"]:
			return
		bout = self.calBout(vic, att, self.buffId)
		buff.addOrReplace(att, self.buffId, bout, vic)


from common import *
import buff
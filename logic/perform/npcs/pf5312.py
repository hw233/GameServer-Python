# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

buffList = [402, 403, 404]

#导表开始
class Perform(CustomPerform):
	id = 5312
	name = "天狐媚术"
	bout = 2
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onSummoned", self.onSummoned)
		
	def onSummoned(self, att, vic):
		buffId = buffList[rand(len(buffList))]
		bout = self.calBout(att, vic, buffId)
		buffObj = buff.addOrReplace(att, buffId, bout, vic)
		if buffObj and buffId == 404:
			hp = int(vic.level * 0.6 + 10)
			buffObj.config(hp)


from common import *
import buff
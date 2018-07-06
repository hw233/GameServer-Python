# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5631
	name = "明睛慧目"
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onMoveDone", self.onMoveDone)
		
	def onMoveDone(self, att, vic, vicCast, dp, attackType):
		self.performSay(att)
		hp = att.calDamageForPhy(vic)
		vic.addHP(-hp, att)
		
from war.defines import *
import perform
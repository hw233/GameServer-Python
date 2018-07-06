# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "洗髓易筋"
	type = BUFF_TYPE_BUFF
#导表结束
	hp = 1

	def onSetup(self, w):
		self.addFunc(w, "onRevive", self.onRevive)
	
	def onCancelSetup(self, w):
		if self.bout <= 0:
			self.cure(w)
	
	def cure(self, w):
		if w.isDead():
			return
		w.addHP(self.hp, w)
		
	def onRevive(self, vic, att):
		if vic.isRole() and hasattr(self, "ratio") and rand(100) < self.ratio:
			pass
		else:
			buff.remove(vic, self.id)
		vic.war.printDebugMsg("\t\t[%s]身上状态[%s]的复活效果生效了" % (vic.name, self.name))
		vic.addHP(self.hp, vic)

from common import *
import buff
# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import MagAttackPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6208
	name = "斩仙御剑术"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 3
	damage = lambda self,hpMaxV:hpMaxV*0.3
	power = 100
	buffId = 921
#导表结束

	def onSetup(self, w):
		self.addFunc(w, "onAddWarrior", self.onAddWarrior)
	
	def onAddWarrior(self, w):
		buff.addOrReplace(w, self.buffId, 99)

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		return self.transCode(self.damage, att, vic)

	def perform(self, att, vicCast):
		warObj = att.war
		if hasattr(warObj.game, "getText"):
			content = warObj.game.getText(7004)
			warObj.say(att,content)

		CustomPerform.perform(self, att, vicCast)
	
	
import buff


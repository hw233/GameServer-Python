# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5119
	name = "吸血"
	configInfo = {
		"生命":20,
	}
#导表结束
#使用物理攻击时，吸取所造成伤害20%的生命，群攻技能只对主目标有吸血效果

	def onSetup(self, w):
		self.addFunc(w, "onAttack", self.onAttack)
		
	def onAttack(self, att, vic, vicCast, dp, attackType):
		if attackType.attackType not in phyAttackTypeList:
			return
		if vic.attackedIdx != 0: # 不是主目标
			return
		hp = dp * self.configInfo["生命"] / 100
		att.addHP(hp)
	
	
from common import *
from war.defines import *
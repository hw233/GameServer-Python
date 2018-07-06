# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5117
	name = "连斩"
	configInfo = {
		"概率":40,
		"伤害结果加成":-15,
	}
#导表结束
#使用普通攻击时，40%几率触发第二次普通攻击，拥有此技能的异兽伤害结果降低15%

	def onSetup(self, w):
		self.addFunc(w, "onPhyAttack", self.onPhyAttack)
		self.addApply(w, "物理伤害结果加成", self.configInfo["伤害结果加成"])
		self.addApply(w, "法术伤害结果加成", self.configInfo["伤害结果加成"])
		
	def onPhyAttack(self, att, vic, attackType):
		if attackType.isBack:
			return
		if rand(100) < self.configInfo["概率"]:
			war.commands.doPhyAttack(att, True)

from common import *
import war.commands

	
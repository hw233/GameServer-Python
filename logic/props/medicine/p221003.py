# -*- coding: utf-8 -*-

import props.medicine

#断续膏
class cProps(props.medicine.cProps):

	def use(self, who):#使用
		message.tips(who,"不能在战斗外使用")
		return False

	def useInWar(self, who, att, vic):#战斗中使用
		if not vic.isDead():
			message.tips(who, "目标不需要复活")
			return False
		if vic.hasApply("禁止复活"):
			message.tips(who, "目标不能被复活")
			return False
		self.addStackInWar(who,att)
		att.war.rpcWarPerform(att, MAGIC_USE_PROPS, vic, self.no())
		ratio = 100 + self.getEffectRatio(att,vic)
		hp = self.getEffect().get("生命")
		if hp:
			vic.addHP(int(hp)*ratio/100)
		return True

import message
from war.defines import *
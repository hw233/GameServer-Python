# -*- coding: utf-8 -*-
from state.object import State as customState

#导表开始
class State(customState):
	no= 102
	name = "自动回复生命"
	info = "剩余生命值：#C03$hp#n"
#导表结束

	def getInfo(self):
		hp = 0
		owner = getRole(self.ownerId)
		if owner:
			hp = owner.reserveHp
		info = self.info.replace("$hp", str(hp))
		return info


from common import *

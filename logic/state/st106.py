# -*- coding: utf-8 -*-
from state.object import State as customState

#导表开始
class State(customState):
	no= 106
	name = "经验加成"
	info = "经验额外加成：#C03$rate#n"
#导表结束

	def getInfo(self):
		ratio = 0
		owner = getRole(self.ownerId)
		if owner:
			ratio = "{}%".format(owner.getExpRatio()-100)
		info = self.info.replace("$rate", ratio)
		return info


from common import *
# -*- coding: utf-8 -*-
from state.object import State as customState

#导表开始
class State(customState):
	no= 101
	name = "高倍经验"
	info = "剩余次数：#C03$number#n"
#导表结束

	def getInfo(self):
		dp = 0
		owner = getRole(self.ownerId)
		if owner:
			dp = owner.doublePoint
		info = self.info.replace("$number", str(dp))
		return info


from common import *

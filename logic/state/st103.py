# -*- coding: utf-8 -*-
from state.object import State as customState

#导表开始
class State(customState):
	no= 103
	name = "自动回复真气"
	info = "剩余真气值：#C03$mp#n"
#导表结束

	def getInfo(self):
		mp = 0
		owner = getRole(self.ownerId)
		if owner:
			mp = owner.reserveMp
		info = self.info.replace("$mp", str(mp))
		return info


from common import *

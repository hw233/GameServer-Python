# -*- coding: utf-8 -*-
from state.object import State as customState

#导表开始
class State(customState):
	no= 104
	name = "装备修理"
	info = ""
#导表结束

	def save(self):
		return None # 不存盘
# -*- coding: utf-8 -*-
'''
元宝
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		who.rewardTradeCash(val, "虚拟道具")
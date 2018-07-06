# -*- coding: utf-8 -*-
'''
银币
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		who.rewardCash(val, "虚拟道具")

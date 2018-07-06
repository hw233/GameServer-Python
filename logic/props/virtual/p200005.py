# -*- coding: utf-8 -*-
'''
降魔积分
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		who.addDemonPoint(val, "虚拟道具")

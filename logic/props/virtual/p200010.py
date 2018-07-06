# -*- coding: utf-8 -*-
'''
献花积分
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		who.addFlowerPoint(val, "虚拟道具")

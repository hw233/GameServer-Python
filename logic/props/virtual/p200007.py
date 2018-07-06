# -*- coding: utf-8 -*-
'''
武勋值
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		who.addPKPoint(val, "虚拟道具")

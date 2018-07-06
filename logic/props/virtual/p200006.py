# -*- coding: utf-8 -*-
'''
侠义值
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		who.addHelpPoint(val, "虚拟道具")

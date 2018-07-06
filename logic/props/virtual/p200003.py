# -*- coding: utf-8 -*-
'''
龙纹玉
'''
import props.virtual


class cProps(props.virtual.cProps):
	def use(self, who):
		val = self.getValue()
		who.addMoneyCash(val, "虚拟道具")
